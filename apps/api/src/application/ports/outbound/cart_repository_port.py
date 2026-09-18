from abc import ABC, abstractmethod
from typing import Optional
from src.domain.model.cart import Cart, CartItem

class CartRepositoryPort(ABC):
    @abstractmethod
    async def get_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Optional[Cart]:
        pass

    @abstractmethod
    async def create_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Cart:
        pass

    @abstractmethod
    async def add_item_to_cart(self, cart_id: str, item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def get_cart_item(self, item_id: str) -> Optional[CartItem]:
        pass

    @abstractmethod
    async def update_cart_item_quantity(self, item_id: str, quantity: int) -> CartItem:
        pass

    @abstractmethod
    async def delete_cart_item(self, item_id: str) -> bool:
        pass

    @abstractmethod
    async def clear_cart(self, cart_id: str) -> bool:
        pass
