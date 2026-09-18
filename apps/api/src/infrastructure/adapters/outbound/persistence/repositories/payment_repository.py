from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.model.payment import Payment, PaymentStatus, PaymentProvider, ProcessedWebhookEvent
from src.application.ports.outbound.payment_repository_port import PaymentRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import PaymentEntity, ProcessedWebhookEntity

class PaymentRepository(PaymentRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, entity: PaymentEntity) -> Payment:
        return Payment(
            id=entity.id,
            order_id=entity.order_id,
            user_id=entity.user_id,
            amount=entity.amount,
            currency=entity.currency,
            status=PaymentStatus(entity.status) if entity.status in PaymentStatus.__members__ else PaymentStatus.INITIATED,
            provider=PaymentProvider(entity.provider) if entity.provider in PaymentProvider.__members__ else PaymentProvider.PAYSTACK,
            provider_reference=entity.provider_reference,
            access_code=entity.access_code,
            checkout_url=entity.checkout_url,
            idempotency_key=entity.idempotency_key,
            channel=entity.channel,
            gateway_response=entity.gateway_response or {},
            failure_reason=entity.failure_reason,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            paid_at=entity.paid_at
        )

    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        stmt = select(PaymentEntity).where(PaymentEntity.id == payment_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def get_by_idempotency_key(self, idempotency_key: str) -> Optional[Payment]:
        stmt = select(PaymentEntity).where(PaymentEntity.idempotency_key == idempotency_key)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def get_by_provider_reference(self, reference: str) -> Optional[Payment]:
        stmt = select(PaymentEntity).where(PaymentEntity.provider_reference == reference)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def save_payment(self, payment: Payment) -> Payment:
        stmt = select(PaymentEntity).where(PaymentEntity.id == payment.id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()

        if not entity:
            entity = PaymentEntity(
                id=payment.id,
                order_id=payment.order_id,
                user_id=payment.user_id,
                amount=payment.amount,
                currency=payment.currency,
                status=payment.status.value,
                provider=payment.provider.value,
                provider_reference=payment.provider_reference,
                access_code=payment.access_code,
                checkout_url=payment.checkout_url,
                idempotency_key=payment.idempotency_key,
                channel=payment.channel,
                gateway_response=payment.gateway_response,
                failure_reason=payment.failure_reason,
                created_at=payment.created_at,
                updated_at=payment.updated_at,
                paid_at=payment.paid_at
            )
            self.session.add(entity)
        else:
            entity.status = payment.status.value
            entity.channel = payment.channel
            entity.gateway_response = payment.gateway_response
            entity.failure_reason = payment.failure_reason
            entity.updated_at = payment.updated_at
            entity.paid_at = payment.paid_at

        await self.session.commit()
        await self.session.refresh(entity)
        return self._to_domain(entity)

    async def is_webhook_processed(self, provider: str, event_id: str) -> bool:
        stmt = select(ProcessedWebhookEntity).where(
            ProcessedWebhookEntity.provider == provider,
            ProcessedWebhookEntity.event_id == event_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def record_webhook_event(self, event: ProcessedWebhookEvent) -> ProcessedWebhookEvent:
        entity = ProcessedWebhookEntity(
            id=event.id,
            provider=event.provider,
            event_id=event.event_id,
            event_type=event.event_type,
            payload_hash=event.payload_hash,
            processed_at=event.processed_at,
            raw_payload=event.raw_payload
        )
        self.session.add(entity)
        await self.session.commit()
        return event
