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

class OPayPaymentProvider(PaymentProvider):
    """
    OPay Merchant Cashier Payment Provider implementation with HMAC-SHA512 signature authentication,
    server-side cashier initialization, query status verification, and webhook handling.
    """

    def __init__(
        self,
        merchant_id: Optional[str] = None,
        secret_key: Optional[str] = None,
        public_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.merchant_id = merchant_id or settings.OPAY_MERCHANT_ID
        self.secret_key = secret_key or settings.OPAY_SECRET_KEY
        self.public_key = public_key or settings.OPAY_PUBLIC_KEY
        self.base_url = (base_url or settings.OPAY_BASE_URL).rstrip("/")
        self.is_mock = self.secret_key.startswith("mock_opay_secret") or not self.secret_key

    @property
    def provider_type(self) -> PaymentProviderType:
        return PaymentProviderType.OPAY

    def _generate_signature(self, request_payload: Dict[str, Any]) -> str:
        """
        OPay HMAC-SHA512 authorization signature generation.
        """
        payload_str = json.dumps(request_payload, separators=(',', ':'))
        return hmac.new(
            self.secret_key.encode("utf-8"),
            payload_str.encode("utf-8"),
            hashlib.sha512
        ).hexdigest()

    async def initialize(self, request: PaymentRequest) -> PaymentInitializationResult:
        # Amount in Kobo or string formatting based on OPay Cashier specification
        amount_kobo = str(int(round(request.amount * 100)))
        provider_ref = f"opay_{request.order_number}_{request.idempotency_key[:8]}"
        callback_url = request.callback_url or f"{settings.FRONTEND_URL}/checkout/verify?gateway=OPAY"

        if self.is_mock:
            checkout_url = f"{callback_url}&reference={provider_ref}&orderNo={provider_ref}&status=SUCCESS"
            return PaymentInitializationResult(
                provider=self.provider_type,
                provider_reference=provider_ref,
                checkout_url=checkout_url,
                access_code=f"opay_cashier_{request.idempotency_key[:10]}",
                raw_response={
                    "code": "00000",
                    "message": "SUCCESS (Mock Mode)",
                    "data": {"cashierUrl": checkout_url, "reference": provider_ref, "orderNo": provider_ref}
                }
            )

        payload = {
            "country": "NG",
            "reference": provider_ref,
            "amount": amount_kobo,
            "currency": request.currency or "NGN",
            "returnUrl": callback_url,
            "callbackUrl": f"{settings.FRONTEND_URL}/api/v1/payments/webhooks/opay",
            "expireAt": "30", # minutes
            "userInfo": {
                "userEmail": request.customer_email,
                "userName": request.customer_name,
                "userMobile": request.customer_phone or "08000000000"
            },
            "product": {
                "name": f"Laptop Store Order #{request.order_number}",
                "description": "High-Performance Custom Laptop & Accessories"
            }
        }

        signature = self._generate_signature(payload)
        headers = {
            "Authorization": f"Bearer {signature}",
            "MerchantId": self.merchant_id,
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(f"{self.base_url}/api/v3/cashier/initialize", json=payload, headers=headers)
                data = res.json()
                if not res.is_success or data.get("code") != "00000":
                    logger.error(f"OPay initialization failed: {data}")
                    raise RuntimeError(f"OPay API error: {data.get('message', 'Failed to initialize OPay cashier')}")

                result_data = data.get("data", {})
                return PaymentInitializationResult(
                    provider=self.provider_type,
                    provider_reference=result_data.get("reference", provider_ref),
                    checkout_url=result_data.get("cashierUrl", ""),
                    access_code=result_data.get("orderNo"),
                    raw_response=data
                )
        except httpx.RequestError as exc:
            logger.error(f"OPay network error: {exc}")
            raise TimeoutError(f"Payment gateway timeout connecting to OPay: {str(exc)}")

    async def verify(self, provider_reference: str) -> PaymentVerificationResult:
        if self.is_mock:
            return PaymentVerificationResult(
                provider=self.provider_type,
                provider_reference=provider_reference,
                status=PaymentStatus.SUCCESS,
                amount=1450000.0,
                currency="NGN",
                channel="opay_wallet_or_qr",
                paid_at=datetime.utcnow(),
                gateway_message="OPay mock payment verified successfully",
                raw_response={"code": "00000", "data": {"status": "SUCCESS", "reference": provider_reference}}
            )

        payload = {
            "reference": provider_reference,
            "country": "NG"
        }
        signature = self._generate_signature(payload)
        headers = {
            "Authorization": f"Bearer {signature}",
            "MerchantId": self.merchant_id,
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(f"{self.base_url}/api/v3/cashier/status", json=payload, headers=headers)
                data = res.json()
                if not res.is_success or data.get("code") != "00000":
                    return PaymentVerificationResult(
                        provider=self.provider_type,
                        provider_reference=provider_reference,
                        status=PaymentStatus.FAILED,
                        amount=0.0,
                        currency="NGN",
                        gateway_message=data.get("message", "OPay status query failed"),
                        raw_response=data
                    )

                tx_data = data.get("data", {})
                opay_status = tx_data.get("status")
                
                status_map = {
                    "SUCCESS": PaymentStatus.SUCCESS,
                    "FAIL": PaymentStatus.FAILED,
                    "PENDING": PaymentStatus.PROCESSING,
                    "CLOSED": PaymentStatus.EXPIRED
                }
                normalized_status = status_map.get(opay_status, PaymentStatus.PROCESSING)
                amount = float(tx_data.get("amount", 0)) / 100.0 if tx_data.get("amount") else 0.0

                return PaymentVerificationResult(
                    provider=self.provider_type,
                    provider_reference=provider_reference,
                    status=normalized_status,
                    amount=amount,
                    currency=tx_data.get("currency", "NGN"),
                    channel=tx_data.get("channel", "OPAY_WALLET"),
                    paid_at=datetime.utcnow() if normalized_status == PaymentStatus.SUCCESS else None,
                    gateway_message=tx_data.get("status", "Status checked"),
                    raw_response=data
                )
        except httpx.RequestError as exc:
            logger.error(f"OPay verification timeout: {exc}")
            raise TimeoutError(f"Gateway timeout verifying OPay reference {provider_reference}: {str(exc)}")

    def verify_webhook_signature(self, raw_body: bytes, headers: Dict[str, str]) -> bool:
        """
        OPay signs webhook callbacks with HMAC-SHA512 using the Merchant Secret Key in 'sha512' or 'Signature' header.
        """
        signature = headers.get("sha512") or headers.get("Sha512") or headers.get("signature") or headers.get("Signature")
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
        payload_data = payload.get("payload") or payload.get("data") or payload
        reference = payload_data.get("reference") or payload_data.get("orderNo", "")
        status_str = payload_data.get("status", "SUCCESS")
        event_id = str(payload_data.get("itemRef") or reference or f"opay_evt_{hashlib.md5(json.dumps(payload, sort_keys=True).encode()).hexdigest()}")

        status_map = {
            "SUCCESS": PaymentStatus.SUCCESS,
            "FAIL": PaymentStatus.FAILED,
            "PENDING": PaymentStatus.PROCESSING
        }
        status = status_map.get(status_str, PaymentStatus.SUCCESS)
        amount_raw = payload_data.get("amount", 0)
        # OPay amounts can be either minor units or direct float
        amount = float(amount_raw) / 100.0 if float(amount_raw) > 1000000 else float(amount_raw)

        return ParsedWebhookEvent(
            provider=self.provider_type,
            event_id=event_id,
            event_type=payload.get("event", "payment.successful"),
            provider_reference=reference,
            status=status,
            amount=amount,
            currency=payload_data.get("currency", "NGN"),
            paid_at=datetime.utcnow(),
            raw_payload=payload
        )
