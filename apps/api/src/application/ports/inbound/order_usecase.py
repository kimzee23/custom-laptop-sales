from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.model.order import Order, OrderStatus

class OrderUseCase(ABC):
    @abstractmethod
    async def create_order(
        self,
        customer_name: str,
        customer_email: str,
        customer_phone: Optional[str],
        shipping_address: Dict[str, Any],
        items: List[Dict[str, Any]],
        user_id: Optional[str] = None
    ) -> Order:
        pass

    @abstractmethod
    async def get_order_by_id_or_number(self, identifier: str) -> Order:
        pass

    @abstractmethod
    async def list_orders(self, user_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Order]:
        pass

    @abstractmethod
    async def update_order_status(self, order_id: str, status: OrderStatus) -> Order:
        pass
