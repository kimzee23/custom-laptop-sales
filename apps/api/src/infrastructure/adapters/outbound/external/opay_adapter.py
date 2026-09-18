import uuid
from typing import Dict, Any
from src.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from src.infrastructure.config.settings import settings

class OPayAdapter(PaymentGatewayPort):
    def __init__(self, merchant_id: str = None, secret_key: str = None, public_key: str = None, base_url: str = None):
        self.merchant_id = merchant_id or settings.OPAY_MERCHANT_ID
        self.secret_key = secret_key or settings.OPAY_SECRET_KEY
        self.public_key = public_key or settings.OPAY_PUBLIC_KEY
        self.base_url = base_url or settings.OPAY_BASE_URL

    async def initialize_transaction(self, order_id: str, amount: float, email: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        reference = f"opay_{order_id}_{uuid.uuid4().hex[:8]}"
        checkout_url = f"https://cashier.opayweb.com/pay/{reference}"

        return {
            "reference": reference,
            "checkout_url": checkout_url,
            "provider": "OPAY"
        }

    async def verify_transaction(self, reference: str) -> Dict[str, Any]:
        return {
            "is_successful": True,
            "amount": 0.0,
            "currency": "NGN",
            "provider": "OPAY",
            "raw_response": {"status": "SUCCESS", "orderNo": reference}
        }
