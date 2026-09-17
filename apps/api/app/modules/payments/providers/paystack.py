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

class PaystackPaymentProvider(PaymentProvider):
    """
    Paystack Payment Provider implementation with HMAC-SHA512 webhook signature verification
    and server-side transaction initialization & verification.
    """

    def __init__(
        self,
        secret_key: Optional[str] = None,
        public_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.secret_key = secret_key or settings.PAYSTACK_SECRET_KEY
        self.public_key = public_key or settings.PAYSTACK_PUBLIC_KEY
        self.base_url = (base_url or settings.PAYSTACK_BASE_URL).rstrip("/")
        self.is_mock = self.secret_key.startswith("sk_test_mock") or not self.secret_key

    @property
    def provider_type(self) -> PaymentProviderType:
        return PaymentProviderType.PAYSTACK

    async def initialize(self, request: PaymentRequest) -> PaymentInitializationResult:
        # Amount in Kobo (1 NGN = 100 Kobo)
        amount_kobo = int(round(request.amount * 100))
        provider_ref = f"pstk_{request.order_number}_{request.idempotency_key[:8]}"
        callback_url = request.callback_url or f"{settings.FRONTEND_URL}/checkout/verify?gateway=PAYSTACK"

        if self.is_mock:
            # Realistic sandbox simulation
            checkout_url = f"{callback_url}&reference={provider_ref}&trxref={provider_ref}&status=success"
            return PaymentInitializationResult(
                provider=self.provider_type,
                provider_reference=provider_ref,
                checkout_url=checkout_url,
                access_code=f"pstk_acc_{request.idempotency_key[:12]}",
                raw_response={"status": True, "message": "Authorization URL created (Mock Mode)", "data": {"authorization_url": checkout_url, "reference": provider_ref}}
            )

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": request.customer_email,
            "amount": amount_kobo,
            "reference": provider_ref,
            "callback_url": callback_url,
            "metadata": {
                "order_id": request.order_id,
                "order_number": request.order_number,
                "customer_name": request.customer_name,
                "idempotency_key": request.idempotency_key,
                **request.metadata
            }
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(f"{self.base_url}/transaction/initialize", json=payload, headers=headers)
                data = res.json()
                if not res.is_success or not data.get("status"):
                    logger.error(f"Paystack initialization failed: {data}")
                    raise RuntimeError(f"Paystack API error: {data.get('message', 'Failed to initialize payment')}")
                
                result_data = data.get("data", {})
                return PaymentInitializationResult(
                    provider=self.provider_type,
                    provider_reference=result_data.get("reference", provider_ref),
                    checkout_url=result_data.get("authorization_url", ""),
                    access_code=result_data.get("access_code"),
                    raw_response=data
                )
        except httpx.RequestError as exc:
            logger.error(f"Paystack network error: {exc}")
            raise TimeoutError(f"Payment gateway timeout connecting to Paystack: {str(exc)}")

    async def verify(self, provider_reference: str) -> PaymentVerificationResult:
        if self.is_mock:
            return PaymentVerificationResult(
                provider=self.provider_type,
                provider_reference=provider_reference,
                status=PaymentStatus.SUCCESS,
                amount=1450000.0,
                currency="NGN",
                channel="card",
                paid_at=datetime.utcnow(),
                gateway_message="Transaction verified successfully (Mock Mode)",
                raw_response={"status": True, "data": {"status": "success", "reference": provider_reference}}
            )

        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.get(f"{self.base_url}/transaction/verify/{provider_reference}", headers=headers)
                data = res.json()
                if not res.is_success or not data.get("status"):
                    return PaymentVerificationResult(
                        provider=self.provider_type,
                        provider_reference=provider_reference,
                        status=PaymentStatus.FAILED,
                        amount=0.0,
                        currency="NGN",
                        gateway_message=data.get("message", "Verification failed"),
                        raw_response=data
                    )

                tx_data = data.get("data", {})
                gateway_status = tx_data.get("status")
                
                status_map = {
                    "success": PaymentStatus.SUCCESS,
                    "failed": PaymentStatus.FAILED,
                    "abandoned": PaymentStatus.EXPIRED,
                    "reversed": PaymentStatus.CANCELLED,
                    "ongoing": PaymentStatus.PROCESSING,
                    "pending": PaymentStatus.PROCESSING
                }
                normalized_status = status_map.get(gateway_status, PaymentStatus.PROCESSING)
                amount = float(tx_data.get("amount", 0)) / 100.0 # Convert from Kobo
                paid_at_str = tx_data.get("paid_at")
                paid_at = datetime.fromisoformat(paid_at_str.replace("Z", "+00:00")) if paid_at_str else None

                return PaymentVerificationResult(
                    provider=self.provider_type,
                    provider_reference=provider_reference,
                    status=normalized_status,
                    amount=amount,
                    currency=tx_data.get("currency", "NGN"),
                    channel=tx_data.get("channel"),
                    paid_at=paid_at,
                    gateway_message=tx_data.get("gateway_response", "Transaction verified"),
                    raw_response=data
                )
        except httpx.RequestError as exc:
            logger.error(f"Paystack verification timeout: {exc}")
            raise TimeoutError(f"Gateway timeout verifying reference {provider_reference}: {str(exc)}")

    def verify_webhook_signature(self, raw_body: bytes, headers: Dict[str, str]) -> bool:
        """
        Paystack signs webhook payloads using HMAC SHA512 with the secret key in 'x-paystack-signature'.
        """
        signature = headers.get("x-paystack-signature") or headers.get("X-Paystack-Signature")
        if not signature:
            if self.is_mock:
                return True
            return False

        computed_hmac = hmac.new(
            self.secret_key.encode("utf-8"),
            raw_body,
            hashlib.sha512
        ).hexdigest()

        return hmac.compare_digest(computed_hmac, signature)

    def parse_webhook(self, payload: Dict[str, Any]) -> ParsedWebhookEvent:
        event_name = payload.get("event", "charge.success")
        data = payload.get("data", {})
        reference = data.get("reference", "")
        event_id = str(data.get("id") or reference or f"pstk_evt_{hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()}")
        status_str = data.get("status", "success")

        status_map = {
            "success": PaymentStatus.SUCCESS,
            "failed": PaymentStatus.FAILED,
            "reversed": PaymentStatus.CANCELLED
        }
        status = status_map.get(status_str, PaymentStatus.SUCCESS if event_name == "charge.success" else PaymentStatus.FAILED)
        amount = float(data.get("amount", 0)) / 100.0

        paid_at_str = data.get("paid_at")
        paid_at = datetime.fromisoformat(paid_at_str.replace("Z", "+00:00")) if paid_at_str else datetime.utcnow()

        return ParsedWebhookEvent(
            provider=self.provider_type,
            event_id=event_id,
            event_type=event_name,
            provider_reference=reference,
            status=status,
            amount=amount,
            currency=data.get("currency", "NGN"),
            paid_at=paid_at,
            raw_payload=payload
        )
