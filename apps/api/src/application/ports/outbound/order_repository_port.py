from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.model.order import Order, OrderStatus

class OrderRepositoryPort(ABC):
    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_by_order_number(self, order_number: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def list_orders(self, user_id: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 50) -> List[Order]:
        pass

    @abstractmethod
    async def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        pass
