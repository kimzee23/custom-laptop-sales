import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import random
from src.domain.model.order import Order, OrderItem, OrderStatus
from src.domain.exception.exceptions import OrderNotFoundException
from src.application.ports.inbound.order_usecase import OrderUseCase
from src.application.ports.inbound.notification_usecase import NotificationUseCase
from src.application.ports.outbound.order_repository_port import OrderRepositoryPort

class OrderService(OrderUseCase):
    def __init__(self, order_repository: OrderRepositoryPort, notification_service: Optional[NotificationUseCase] = None):
        self.order_repo = order_repository
        self.notification_service = notification_service

    def _generate_order_number(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        rand = random.randint(1000, 9999)
        return f"ORD-{date_str}-{rand}"

    async def create_order(
        self,
        customer_name: str,
        customer_email: str,
        customer_phone: Optional[str],
        shipping_address: Dict[str, Any],
        items: List[Dict[str, Any]],
        user_id: Optional[str] = None
    ) -> Order:
        order_id = str(uuid.uuid4())
        order_number = self._generate_order_number()

        order_items = []
        subtotal = 0.0
        for it in items:
            qty = it.get("quantity", 1)
            unit_price = float(it.get("unit_price", 0.0))
            line_total = unit_price * qty
            subtotal += line_total
            order_items.append(OrderItem(
                id=str(uuid.uuid4()),
                order_id=order_id,
                product_id=it["product_id"],
                quantity=qty,
                unit_price=unit_price,
                total_price=line_total,
                configuration_snapshot=it.get("configuration_snapshot", {}),
                product_title=it.get("product_title"),
                product_image=it.get("product_image")
            ))

        shipping_fee = 0.0
        total_amount = subtotal + shipping_fee

        order = Order(
            id=order_id,
            order_number=order_number,
            user_id=user_id,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            discount_amount=0.0,
            total_amount=total_amount,
            currency="NGN",
            status=OrderStatus.PENDING_PAYMENT,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            items=order_items
        )
        saved_order = await self.order_repo.create_order(order)

        if self.notification_service:
            try:
                await self.notification_service.send_order_confirmation_email({
                    "customer_email": saved_order.customer_email,
                    "customer_name": saved_order.customer_name,
                    "order_number": saved_order.order_number,
                    "total_amount": saved_order.total_amount,
                    "status": saved_order.status.value if hasattr(saved_order.status, "value") else str(saved_order.status),
                    "items": [
                        {
                            "title": it.product_title or "Custom Laptop Item",
                            "quantity": it.quantity,
                            "total_price": it.total_price
                        }
                        for it in saved_order.items
                    ]
                })
            except Exception as e:
                import logging
                logging.getLogger("order_service").error(f"Failed to dispatch order confirmation email: {e}")

        return saved_order

    async def get_order_by_id_or_number(self, identifier: str) -> Order:
        order = await self.order_repo.get_by_id(identifier)
        if not order:
            order = await self.order_repo.get_by_order_number(identifier)
        if not order:
            raise OrderNotFoundException(f"Order '{identifier}' not found.")
        return order

    async def list_orders(self, user_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Order]:
        skip = (page - 1) * page_size
        return await self.order_repo.list_orders(user_id=user_id, skip=skip, limit=page_size)

    async def update_order_status(self, order_id: str, status: OrderStatus) -> Order:
        order = await self.order_repo.update_status(order_id, status)
        if not order:
            raise OrderNotFoundException(f"Order '{order_id}' not found.")

        if self.notification_service:
            try:
                status_str = status.value if hasattr(status, "value") else str(status)
                await self.notification_service.send_order_tracking_email(
                    order_data={
                        "customer_email": order.customer_email,
                        "customer_name": order.customer_name,
                        "order_number": order.order_number
                    },
                    tracking_status=status_str,
                    tracking_note=f"Your order status is now {status_str}."
                )
            except Exception as e:
                import logging
                logging.getLogger("order_service").error(f"Failed to dispatch order tracking email: {e}")

        return order
