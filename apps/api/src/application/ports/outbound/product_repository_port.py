from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.model.product import Product, Category, Brand, Promotion

class ProductRepositoryPort(ABC):
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
        skip: int = 0,
        limit: int = 20
    ) -> List[Product]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def save_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def delete_product(self, product_id: str) -> bool:
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
