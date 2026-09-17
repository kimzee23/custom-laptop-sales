import logging
from typing import Callable, List, Any
from app.modules.payments.domain.models import PaymentCompletedEvent

logger = logging.getLogger(__name__)

# Type for event handler callback
EventHandler = Callable[..., Any]

class PaymentEventDispatcher:
    """
    In-memory async event dispatcher for payment domain events.
    Decouples payment processing from downstream order fulfillment and enrollment.
    """
    _handlers: List[EventHandler] = []

    @classmethod
    def subscribe(cls, handler: EventHandler):
        if handler not in cls._handlers:
            cls._handlers.append(handler)

    @classmethod
    async def publish_payment_completed(cls, event: PaymentCompletedEvent, db=None):
        logger.info(f"Publishing PaymentCompletedEvent for Order #{event.order_number} (Ref: {event.provider_reference})")
        for handler in cls._handlers:
            try:
                await handler(event, db=db)
            except Exception as e:
                logger.error(f"Error in PaymentCompletedEvent handler: {e}", exc_info=True)
