from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.model.product import Product, Category, Brand, Promotion

class ProductUseCase(ABC):
    @abstractmethod
    async def list_products(
        self,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        featured: Optional[bool] = None,
        flash_deals: Optional[bool] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[Product]:
        pass

    @abstractmethod
    async def get_product_by_id_or_slug(self, identifier: str) -> Product:
        pass

    @abstractmethod
    async def list_categories(self) -> List[Category]:
        pass

    @abstractmethod
    async def list_brands(self) -> List[Brand]:
        pass

    @abstractmethod
    async def list_promotions(self) -> List[Promotion]:
        pass
