from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.domain.model.cart import Cart, CartItem

class CartUseCase(ABC):
    @abstractmethod
    async def get_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Cart:
        pass

    @abstractmethod
    async def add_item(
        self,
        session_id: Optional[str],
        user_id: Optional[str],
        product_id: str,
        quantity: int,
        unit_price: float,
        configuration_data: Dict[str, Any]
    ) -> CartItem:
        pass

    @abstractmethod
    async def update_item_quantity(self, item_id: str, quantity: int) -> CartItem:
        pass

    @abstractmethod
    async def remove_item(self, item_id: str) -> bool:
        pass

    @abstractmethod
    async def clear_cart(self, session_id: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        pass
