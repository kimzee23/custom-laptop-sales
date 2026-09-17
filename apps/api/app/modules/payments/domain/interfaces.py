from typing import Protocol, Dict, Any, Tuple
from app.modules.payments.domain.models import (
    PaymentRequest,
    PaymentInitializationResult,
    PaymentVerificationResult,
    ParsedWebhookEvent,
    PaymentProviderType
)

class PaymentProvider(Protocol):
    """
    Core Payment Provider interface abstraction.
    All payment gateways (Paystack, Flutterwave, OPay) implement this contract.
    Business logic and PaymentService depend strictly on this abstraction.
    """
    
    @property
    def provider_type(self) -> PaymentProviderType:
        """Returns provider identifier enum."""
        ...

    async def initialize(self, request: PaymentRequest) -> PaymentInitializationResult:
        """
        Initializes transaction with gateway and generates checkout redirect URL.
        """
        ...

    async def verify(self, provider_reference: str) -> PaymentVerificationResult:
        """
        Performs authoritative server-to-server query against gateway to verify transaction state.
        """
        ...

    def verify_webhook_signature(self, raw_body: bytes, headers: Dict[str, str]) -> bool:
        """
        Verifies cryptographic signature (HMAC-SHA512 or secret hash) of incoming webhook.
        """
        ...

    def parse_webhook(self, payload: Dict[str, Any]) -> ParsedWebhookEvent:
        """
        Standardizes provider webhook payload into normalized ParsedWebhookEvent domain object.
        """
        ...
