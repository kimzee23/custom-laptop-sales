import uuid
from typing import Dict, Any
from src.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from src.infrastructure.config.settings import settings

class BankTransferAdapter(PaymentGatewayPort):
    def __init__(self, bank_name: str = None, account_name: str = None, account_number: str = None):
        self.bank_name = bank_name or settings.COMPANY_BANK_NAME
        self.account_name = account_name or settings.COMPANY_ACCOUNT_NAME
        self.account_number = account_number or settings.COMPANY_ACCOUNT_NUMBER

    async def initialize_transaction(self, order_id: str, amount: float, email: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        reference = f"bt_{order_id}_{uuid.uuid4().hex[:8]}"

        return {
            "reference": reference,
            "bank_name": self.bank_name,
            "account_name": self.account_name,
            "account_number": self.account_number,
            "instructions": f"Please transfer NGN {amount:,.2f} to {self.bank_name}, Account {self.account_number} ({self.account_name}) with reference {reference}.",
            "provider": "BANK_TRANSFER"
        }

    async def verify_transaction(self, reference: str) -> Dict[str, Any]:
        return {
            "is_successful": True,
            "amount": 0.0,
            "currency": "NGN",
            "provider": "BANK_TRANSFER",
            "raw_response": {"status": "manual_review", "reference": reference}
        }
