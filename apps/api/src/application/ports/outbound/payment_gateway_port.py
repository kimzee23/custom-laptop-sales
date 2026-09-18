from abc import ABC, abstractmethod
from typing import Dict, Any

class PaymentGatewayPort(ABC):
    @abstractmethod
    async def initialize_transaction(self, order_id: str, amount: float, email: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Returns { 'reference': str, 'checkout_url': str, 'access_code': Optional[str] }"""
        pass

    @abstractmethod
    async def verify_transaction(self, reference: str) -> Dict[str, Any]:
        """Returns { 'is_successful': bool, 'amount': float, 'currency': str, 'raw_response': dict }"""
        pass
