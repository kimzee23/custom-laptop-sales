import uuid
from typing import Dict, Any
from src.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from src.infrastructure.config.settings import settings

class FlutterwaveAdapter(PaymentGatewayPort):
    def __init__(self, secret_key: str = None, public_key: str = None, base_url: str = None):
        self.secret_key = secret_key or settings.FLUTTERWAVE_SECRET_KEY
        self.public_key = public_key or settings.FLUTTERWAVE_PUBLIC_KEY
        self.base_url = base_url or settings.FLUTTERWAVE_BASE_URL

    async def initialize_transaction(self, order_id: str, amount: float, email: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        tx_ref = f"flw_{order_id}_{uuid.uuid4().hex[:8]}"
        checkout_url = f"https://ravemodal-dev.herokuapp.com/v3/hosted/pay/{tx_ref}"

        return {
            "reference": tx_ref,
            "checkout_url": checkout_url,
            "provider": "FLUTTERWAVE"
        }

    async def verify_transaction(self, reference: str) -> Dict[str, Any]:
        return {
            "is_successful": True,
            "amount": 0.0,
            "currency": "NGN",
            "provider": "FLUTTERWAVE",
            "raw_response": {"status": "successful", "tx_ref": reference}
        }
