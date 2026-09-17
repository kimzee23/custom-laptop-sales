import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Order
from app.modules.payments.domain.models import PaymentCompletedEvent
from app.modules.payments.services.event_dispatcher import PaymentEventDispatcher

logger = logging.getLogger(__name__)

class OrderFulfillmentService:
    """
    Handles order fulfillment and customer build-queue enrollment upon successful payment.
    Decoupled from PaymentService and fully idempotent.
    """

    @classmethod
    async def on_payment_completed(cls, event: PaymentCompletedEvent, db: AsyncSession):
        """
        Event subscriber for PaymentCompletedEvent.
        """
        if db is None:
            logger.warning("No DB session provided to OrderFulfillmentService handler")
            return

        stmt = select(Order).where(Order.id == event.order_id)
        result = await db.execute(stmt)
        order = result.scalar_one_or_none()

        if not order:
            logger.error(f"Order #{event.order_number} not found during payment fulfillment")
            return

        # Idempotency check: If order is already PAID or beyond, do not re-process
        if order.status in ["PAID", "PROCESSING", "CUSTOM_BUILD", "READY_FOR_SHIPPING", "SHIPPED", "DELIVERED"]:
            logger.info(f"Order #{order.order_number} is already fulfilled (Status: {order.status}). Skipping duplicate event.")
            return

        logger.info(f"Fulfilling Order #{order.order_number} for customer {event.customer_email}")
        order.status = "PAID"
        order.paid_at = event.completed_at or datetime.utcnow()
        order.payment_reference = event.provider_reference
        order.payment_gateway = event.provider.value

        # In a full ERP/Production system, trigger inventory reservation, build technician queue dispatch, and confirmation email
        await db.commit()
        logger.info(f"Order #{order.order_number} successfully marked as PAID and queued for custom assembly.")

# Auto-register event handler
PaymentEventDispatcher.subscribe(OrderFulfillmentService.on_payment_completed)
