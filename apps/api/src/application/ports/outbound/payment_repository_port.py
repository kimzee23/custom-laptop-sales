from abc import ABC, abstractmethod
from typing import Optional
from src.domain.model.payment import Payment, ProcessedWebhookEvent

class PaymentRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def get_by_provider_reference(self, reference: str) -> Optional[Payment]:
        pass

    @abstractmethod
    async def save_payment(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def is_webhook_processed(self, provider: str, event_id: str) -> bool:
        pass

    @abstractmethod
    async def record_webhook_event(self, event: ProcessedWebhookEvent) -> ProcessedWebhookEvent:
        pass
