import uuid
from typing import Dict, Any
from src.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from src.infrastructure.config.settings import settings

class PaystackAdapter(PaymentGatewayPort):
    def __init__(self, secret_key: str = None, public_key: str = None, base_url: str = None):
        self.secret_key = secret_key or settings.PAYSTACK_SECRET_KEY
        self.public_key = public_key or settings.PAYSTACK_PUBLIC_KEY
        self.base_url = base_url or settings.PAYSTACK_BASE_URL

    async def initialize_transaction(self, order_id: str, amount: float, email: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        reference = f"pstk_{order_id}_{uuid.uuid4().hex[:8]}"
        access_code = f"acc_{uuid.uuid4().hex[:12]}"
        checkout_url = f"https://checkout.paystack.com/{access_code}"

        return {
            "reference": reference,
            "access_code": access_code,
            "checkout_url": checkout_url,
            "provider": "PAYSTACK"
        }

    async def verify_transaction(self, reference: str) -> Dict[str, Any]:
        return {
            "is_successful": True,
            "amount": 0.0,
            "currency": "NGN",
            "provider": "PAYSTACK",
            "raw_response": {"status": "success", "reference": reference}
        }
