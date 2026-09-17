import hmac
import hashlib
import json
import logging
import httpx
from datetime import datetime
from typing import Dict, Any, Optional

from app.core.config import settings
from app.modules.payments.domain.models import (
    PaymentRequest,
    PaymentInitializationResult,
    PaymentVerificationResult,
    ParsedWebhookEvent,
    PaymentStatus,
    PaymentProviderType
)
from app.modules.payments.domain.interfaces import PaymentProvider

logger = logging.getLogger(__name__)

class FlutterwavePaymentProvider(PaymentProvider):
    """
    Flutterwave v3 Payment Provider implementation with secret hash webhook verification
    and server-side transaction initialization & verification.
    """

    def __init__(
        self,
        secret_key: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_hash: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.secret_key = secret_key or settings.FLUTTERWAVE_SECRET_KEY
        self.public_key = public_key or settings.FLUTTERWAVE_PUBLIC_KEY
        self.secret_hash = secret_hash or settings.FLUTTERWAVE_SECRET_HASH
        self.base_url = (base_url or settings.FLUTTERWAVE_BASE_URL).rstrip("/")
        self.is_mock = self.secret_key.startswith("FLWSECK_TEST-mock") or not self.secret_key

    @property
    def provider_type(self) -> PaymentProviderType:
        return PaymentProviderType.FLUTTERWAVE

    async def initialize(self, request: PaymentRequest) -> PaymentInitializationResult:
        provider_ref = f"flw_{request.order_number}_{request.idempotency_key[:8]}"
        redirect_url = request.callback_url or f"{settings.FRONTEND_URL}/checkout/verify?gateway=FLUTTERWAVE"

        if self.is_mock:
            checkout_url = f"{redirect_url}&tx_ref={provider_ref}&status=successful"
            return PaymentInitializationResult(
                provider=self.provider_type,
                provider_reference=provider_ref,
                checkout_url=checkout_url,
                access_code=f"flw_link_{request.idempotency_key[:12]}",
                raw_response={"status": "success", "message": "Hosted Link Created (Mock Mode)", "data": {"link": checkout_url}}
            )

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "tx_ref": provider_ref,
            "amount": str(request.amount),
            "currency": request.currency or "NGN",
            "redirect_url": redirect_url,
            "customer": {
                "email": request.customer_email,
                "phonenumber": request.customer_phone or "08000000000",
                "name": request.customer_name
            },
            "customizations": {
                "title": "Custom Laptop Store Checkout",
                "description": f"Payment for Order #{request.order_number}",
                "logo": f"{settings.FRONTEND_URL}/logo.png"
            },
            "meta": {
                "order_id": request.order_id,
                "order_number": request.order_number,
                "idempotency_key": request.idempotency_key,
                **request.metadata
            }
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(f"{self.base_url}/payments", json=payload, headers=headers)
                data = res.json()
                if not res.is_success or data.get("status") != "success":
                    logger.error(f"Flutterwave initialization failed: {data}")
                    raise RuntimeError(f"Flutterwave API error: {data.get('message', 'Failed to initialize payment')}")

                result_data = data.get("data", {})
                return PaymentInitializationResult(
                    provider=self.provider_type,
                    provider_reference=provider_ref,
                    checkout_url=result_data.get("link", ""),
                    access_code=provider_ref,
                    raw_response=data
                )
        except httpx.RequestError as exc:
            logger.error(f"Flutterwave network error: {exc}")
            raise TimeoutError(f"Payment gateway timeout connecting to Flutterwave: {str(exc)}")

    async def verify(self, provider_reference: str) -> PaymentVerificationResult:
        if self.is_mock:
            return PaymentVerificationResult(
                provider=self.provider_type,
                provider_reference=provider_reference,
                status=PaymentStatus.SUCCESS,
                amount=1450000.0,
                currency="NGN",
                channel="ussd_or_card",
                paid_at=datetime.utcnow(),
                gateway_message="Flutterwave mock payment verified successfully",
                raw_response={"status": "success", "data": {"status": "successful", "tx_ref": provider_reference}}
            )

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                # Query by tx_ref
                res = await client.get(
                    f"{self.base_url}/transactions/verify_by_reference",
                    params={"tx_ref": provider_reference},
                    headers=headers
                )
                data = res.json()
                if not res.is_success or data.get("status") != "success":
                    return PaymentVerificationResult(
                        provider=self.provider_type,
                        provider_reference=provider_reference,
                        status=PaymentStatus.FAILED,
                        amount=0.0,
                        currency="NGN",
                        gateway_message=data.get("message", "Flutterwave verification failed"),
                        raw_response=data
                    )

                tx_data = data.get("data", {})
                tx_status = tx_data.get("status")
                status_map = {
                    "successful": PaymentStatus.SUCCESS,
                    "failed": PaymentStatus.FAILED,
                    "cancelled": PaymentStatus.CANCELLED,
                    "pending": PaymentStatus.PROCESSING
                }
                normalized_status = status_map.get(tx_status, PaymentStatus.PROCESSING)
                amount = float(tx_data.get("amount", 0))

                return PaymentVerificationResult(
                    provider=self.provider_type,
                    provider_reference=provider_reference,
                    status=normalized_status,
                    amount=amount,
                    currency=tx_data.get("currency", "NGN"),
                    channel=tx_data.get("payment_type"),
                    paid_at=datetime.utcnow() if normalized_status == PaymentStatus.SUCCESS else None,
                    gateway_message=tx_data.get("processor_response", "Transaction verified"),
                    raw_response=data
                )
        except httpx.RequestError as exc:
            logger.error(f"Flutterwave verification timeout: {exc}")
            raise TimeoutError(f"Gateway timeout verifying Flutterwave reference {provider_reference}: {str(exc)}")

    def verify_webhook_signature(self, raw_body: bytes, headers: Dict[str, str]) -> bool:
        """
        Flutterwave provides secret hash in 'verif-hash' header.
        """
        signature = headers.get("verif-hash") or headers.get("Verif-Hash")
        if not signature:
            if self.is_mock:
                return True
            return False
        return hmac.compare_digest(signature, self.secret_hash)

    def parse_webhook(self, payload: Dict[str, Any]) -> ParsedWebhookEvent:
        event_name = payload.get("event", "charge.completed")
        data = payload.get("data", {})
        tx_ref = data.get("tx_ref", "")
        event_id = str(data.get("id") or tx_ref or f"flw_evt_{hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()}")
        status_str = data.get("status", "successful")

        status_map = {
            "successful": PaymentStatus.SUCCESS,
            "failed": PaymentStatus.FAILED,
            "cancelled": PaymentStatus.CANCELLED
        }
        status = status_map.get(status_str, PaymentStatus.SUCCESS if status_str == "successful" else PaymentStatus.FAILED)
        amount = float(data.get("amount", 0))

        return ParsedWebhookEvent(
            provider=self.provider_type,
            event_id=event_id,
            event_type=event_name,
            provider_reference=tx_ref,
            status=status,
            amount=amount,
            currency=data.get("currency", "NGN"),
            paid_at=datetime.utcnow(),
            raw_payload=payload
        )
