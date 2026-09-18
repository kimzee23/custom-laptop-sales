from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from src.domain.model.order import Order, OrderItem, OrderStatus
from src.application.ports.outbound.order_repository_port import OrderRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import OrderEntity, OrderItemEntity

class OrderRepository(OrderRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, entity: OrderEntity) -> Order:
        items = []
        if "items" in entity.__dict__:
            for it in entity.items:
                product_title = None
                product_image = None
                if "product" in it.__dict__ and it.product:
                    product_title = it.product.title
                    product_image = it.product.image_url
                items.append(
                    OrderItem(
                        id=it.id,
                        order_id=it.order_id,
                        product_id=it.product_id,
                        quantity=it.quantity,
                        unit_price=it.unit_price,
                        total_price=it.total_price,
                        configuration_snapshot=it.configuration_snapshot or {},
                        product_title=product_title,
                        product_image=product_image
                    )
                )
        return Order(
            id=entity.id,
            order_number=entity.order_number,
            user_id=entity.user_id,
            customer_name=entity.customer_name,
            customer_email=entity.customer_email,
            customer_phone=entity.customer_phone,
            shipping_address=entity.shipping_address or {},
            subtotal=entity.subtotal,
            shipping_fee=entity.shipping_fee,
            discount_amount=entity.discount_amount,
            total_amount=entity.total_amount,
            currency=entity.currency,
            status=OrderStatus(entity.status) if entity.status in OrderStatus.__members__ else OrderStatus.PENDING_PAYMENT,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            paid_at=entity.paid_at,
            payment_reference=entity.payment_reference,
            payment_gateway=entity.payment_gateway,
            items=items
        )

    async def create_order(self, order: Order) -> Order:
        stmt = select(OrderEntity).where(OrderEntity.id == order.id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()

        if not entity:
            entity = OrderEntity(
                id=order.id,
                order_number=order.order_number,
                user_id=order.user_id,
                customer_name=order.customer_name,
                customer_email=order.customer_email,
                customer_phone=order.customer_phone,
                shipping_address=order.shipping_address,
                subtotal=order.subtotal,
                shipping_fee=order.shipping_fee,
                discount_amount=order.discount_amount,
                total_amount=order.total_amount,
                currency=order.currency,
                status=order.status.value,
                created_at=order.created_at,
                updated_at=order.updated_at,
                payment_reference=order.payment_reference,
                payment_gateway=order.payment_gateway
            )
            self.session.add(entity)

            for item in order.items:
                it_entity = OrderItemEntity(
                    id=item.id,
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price,
                    configuration_snapshot=item.configuration_snapshot
                )
                self.session.add(it_entity)
        else:
            entity.status = order.status.value
            entity.payment_reference = order.payment_reference
            entity.payment_gateway = order.payment_gateway
            entity.updated_at = order.updated_at

        await self.session.commit()
        return order

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        stmt = select(OrderEntity).options(
            selectinload(OrderEntity.items).selectinload(OrderItemEntity.product)
        ).where(OrderEntity.id == order_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def get_by_order_number(self, order_number: str) -> Optional[Order]:
        stmt = select(OrderEntity).options(
            selectinload(OrderEntity.items).selectinload(OrderItemEntity.product)
        ).where(OrderEntity.order_number == order_number)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def list_orders(self, user_id: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 50) -> List[Order]:
        stmt = select(OrderEntity).options(
            selectinload(OrderEntity.items).selectinload(OrderItemEntity.product)
        )
        if user_id:
            stmt = stmt.where(OrderEntity.user_id == user_id)
        if status:
            stmt = stmt.where(OrderEntity.status == status)

        stmt = stmt.order_by(desc(OrderEntity.created_at)).offset(skip).limit(limit)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [self._to_domain(e) for e in entities]

    async def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        stmt = select(OrderEntity).where(OrderEntity.id == order_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity:
            entity.status = status.value
            import datetime
            entity.updated_at = datetime.datetime.now(datetime.timezone.utc)
            if status == OrderStatus.PAID:
                entity.paid_at = datetime.datetime.now(datetime.timezone.utc)
            await self.session.commit()
            return await self.get_by_id(order_id)
        return None
