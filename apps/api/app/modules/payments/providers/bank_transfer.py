import logging
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

class BankTransferPaymentProvider(PaymentProvider):
    """
    Direct Company Bank Account Payment Provider.
    Facilitates direct bank transfer to company's corporate or personal bank account.
    """

    def __init__(self):
        self.bank_name = settings.COMPANY_BANK_NAME
        self.account_name = settings.COMPANY_ACCOUNT_NAME
        self.account_number = settings.COMPANY_ACCOUNT_NUMBER
        self.whatsapp_number = settings.COMPANY_WHATSAPP_NUMBER

    @property
    def provider_type(self) -> PaymentProviderType:
        return PaymentProviderType.BANK_TRANSFER

    async def initialize(self, request: PaymentRequest) -> PaymentInitializationResult:
        provider_ref = f"bt_{request.order_number}_{request.idempotency_key[:8]}"
        callback_url = request.callback_url or f"{settings.FRONTEND_URL}/checkout/verify?gateway=BANK_TRANSFER"
        checkout_url = f"{callback_url}&reference={provider_ref}&status=pending_transfer"

        bank_details = {
            "bank_name": self.bank_name,
            "account_name": self.account_name,
            "account_number": self.account_number,
            "whatsapp_confirmation": self.whatsapp_number,
            "reference": provider_ref,
            "instructions": f"Transfer exact order total to {self.bank_name} - {self.account_number} ({self.account_name}) using reference '{provider_ref}'. Send payment receipt to WhatsApp {self.whatsapp_number} for immediate clearance."
        }

        return PaymentInitializationResult(
            provider=self.provider_type,
            provider_reference=provider_ref,
            checkout_url=checkout_url,
            access_code=None,
            raw_response={
                "status": True,
                "message": "Direct bank transfer instructions generated",
                "bank_details": bank_details
            }
        )

    async def verify(self, provider_reference: str) -> PaymentVerificationResult:
        # Bank transfers are manually approved or simulated
        return PaymentVerificationResult(
            provider=self.provider_type,
            provider_reference=provider_reference,
            status=PaymentStatus.PROCESSING,
            amount=0.0,
            currency="NGN",
            channel="bank_transfer",
            paid_at=None,
            gateway_message="Direct bank transfer pending confirmation receipt.",
            raw_response={"status": "pending_confirmation", "reference": provider_reference}
        )

    def verify_webhook_signature(self, raw_body: bytes, headers: Dict[str, str]) -> bool:
        return True

    def parse_webhook(self, payload: Dict[str, Any]) -> ParsedWebhookEvent:
        return ParsedWebhookEvent(
            provider=self.provider_type,
            event_id=str(payload.get("reference", "bt_event")),
            event_type="transfer.received",
            provider_reference=str(payload.get("reference", "")),
            status=PaymentStatus.SUCCESS,
            amount=float(payload.get("amount", 0.0)),
            currency="NGN",
            paid_at=datetime.utcnow(),
            raw_payload=payload
        )
