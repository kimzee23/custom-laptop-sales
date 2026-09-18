import uuid
from typing import Optional, Dict, Any
from src.domain.model.cart import Cart, CartItem
from src.domain.exception.exceptions import CartItemNotFoundException
from src.application.ports.inbound.cart_usecase import CartUseCase
from src.application.ports.outbound.cart_repository_port import CartRepositoryPort

class CartService(CartUseCase):
    def __init__(self, cart_repository: CartRepositoryPort):
        self.cart_repo = cart_repository

    async def get_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Cart:
        cart = await self.cart_repo.get_cart(session_id=session_id, user_id=user_id)
        if not cart:
            cart = await self.cart_repo.create_cart(session_id=session_id, user_id=user_id)
        return cart

    async def add_item(
        self,
        session_id: Optional[str],
        user_id: Optional[str],
        product_id: str,
        quantity: int,
        unit_price: float,
        configuration_data: Dict[str, Any]
    ) -> CartItem:
        cart = await self.get_cart(session_id=session_id, user_id=user_id)
        total_price = unit_price * quantity
        item = CartItem(
            id=str(uuid.uuid4()),
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            configuration_data=configuration_data
        )
        return await self.cart_repo.add_item_to_cart(cart.id, item)

    async def update_item_quantity(self, item_id: str, quantity: int) -> CartItem:
        existing = await self.cart_repo.get_cart_item(item_id)
        if not existing:
            raise CartItemNotFoundException(f"Cart item {item_id} not found.")
        return await self.cart_repo.update_cart_item_quantity(item_id, quantity)

    async def remove_item(self, item_id: str) -> bool:
        return await self.cart_repo.delete_cart_item(item_id)

    async def clear_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        cart = await self.cart_repo.get_cart(session_id=session_id, user_id=user_id)
        if cart:
            return await self.cart_repo.clear_cart(cart.id)
        return True
