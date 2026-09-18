from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.domain.model.order import Order
from src.domain.model.product import Product
from src.domain.model.user import User

class AdminUseCase(ABC):
    @abstractmethod
    async def get_dashboard_summary(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def list_all_orders(self, status: Optional[str] = None, page: int = 1, page_size: int = 50) -> List[Order]:
        pass

    @abstractmethod
    async def list_all_customers(self, page: int = 1, page_size: int = 50) -> List[User]:
        pass

    @abstractmethod
    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        pass

    @abstractmethod
    async def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Product:
        pass

    @abstractmethod
    async def delete_product(self, product_id: str) -> bool:
        pass
