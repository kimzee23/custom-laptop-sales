from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload
from src.domain.model.cart import Cart, CartItem
from src.application.ports.outbound.cart_repository_port import CartRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import CartEntity, CartItemEntity

class CartRepository(CartRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, entity: CartEntity) -> Cart:
        items = []
        if "items" in entity.__dict__:
            for it in entity.items:
                product_title = None
                product_image = None
                if "product" in it.__dict__ and it.product:
                    product_title = it.product.title
                    product_image = it.product.image_url
                items.append(
                    CartItem(
                        id=it.id,
                        cart_id=it.cart_id,
                        product_id=it.product_id,
                        quantity=it.quantity,
                        unit_price=it.unit_price,
                        total_price=it.total_price,
                        configuration_data=it.configuration_data or {},
                        product_title=product_title,
                        product_image=product_image
                    )
                )
        return Cart(
            id=entity.id,
            user_id=entity.user_id,
            session_id=entity.session_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            items=items
        )

    async def get_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Optional[Cart]:
        stmt = select(CartEntity).options(
            selectinload(CartEntity.items).selectinload(CartItemEntity.product)
        )
        if user_id:
            stmt = stmt.where(CartEntity.user_id == user_id)
        elif session_id:
            stmt = stmt.where(CartEntity.session_id == session_id)
        else:
            return None

        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def create_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Cart:
        import uuid
        from datetime import datetime, timezone
        entity = CartEntity(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id=session_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return self._to_domain(entity)

    async def add_item_to_cart(self, cart_id: str, item: CartItem) -> CartItem:
        entity = CartItemEntity(
            id=item.id,
            cart_id=cart_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price,
            configuration_data=item.configuration_data
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return item

    async def get_cart_item(self, item_id: str) -> Optional[CartItem]:
        stmt = select(CartItemEntity).where(CartItemEntity.id == item_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if not entity:
            return None
        return CartItem(
            id=entity.id,
            cart_id=entity.cart_id,
            product_id=entity.product_id,
            quantity=entity.quantity,
            unit_price=entity.unit_price,
            total_price=entity.total_price,
            configuration_data=entity.configuration_data or {}
        )

    async def update_cart_item_quantity(self, item_id: str, quantity: int) -> CartItem:
        stmt = select(CartItemEntity).where(CartItemEntity.id == item_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity:
            entity.quantity = quantity
            entity.total_price = entity.unit_price * quantity
            await self.session.commit()
            await self.session.refresh(entity)
            return CartItem(
                id=entity.id,
                cart_id=entity.cart_id,
                product_id=entity.product_id,
                quantity=entity.quantity,
                unit_price=entity.unit_price,
                total_price=entity.total_price,
                configuration_data=entity.configuration_data or {}
            )
        return None

    async def delete_cart_item(self, item_id: str) -> bool:
        stmt = select(CartItemEntity).where(CartItemEntity.id == item_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity:
            await self.session.delete(entity)
            await self.session.commit()
            return True
        return False

    async def clear_cart(self, cart_id: str) -> bool:
        stmt = select(CartItemEntity).where(CartItemEntity.cart_id == cart_id)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        for e in entities:
            await self.session.delete(e)
        await self.session.commit()
        return True
