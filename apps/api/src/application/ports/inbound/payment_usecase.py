from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.domain.model.payment import Payment, PaymentProvider

class PaymentUseCase(ABC):
    @abstractmethod
    async def initialize_payment(
        self,
        order_id: str,
        provider: PaymentProvider,
        idempotency_key: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def verify_payment(self, reference: str, provider: PaymentProvider) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def handle_webhook(self, provider: PaymentProvider, event_id: str, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_supported_gateways(self) -> Dict[str, Any]:
        pass
