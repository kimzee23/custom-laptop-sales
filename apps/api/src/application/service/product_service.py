from typing import List, Optional, Dict, Any
from src.domain.model.product import Product, Category, Brand, Promotion
from src.domain.exception.exceptions import ProductNotFoundException
from src.application.ports.inbound.product_usecase import ProductUseCase
from src.application.ports.outbound.product_repository_port import ProductRepositoryPort

class ProductService(ProductUseCase):
    def __init__(self, product_repository: ProductRepositoryPort):
        self.product_repo = product_repository

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
        skip = (page - 1) * page_size
        return await self.product_repo.list_products(
            category=category,
            brand=brand,
            featured=featured,
            flash_deals=flash_deals,
            search=search,
            sort=sort,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=page_size
        )

    async def get_product_by_id_or_slug(self, identifier: str) -> Product:
        product = await self.product_repo.get_by_id(identifier)
        if not product:
            product = await self.product_repo.get_by_slug(identifier)
        if not product:
            raise ProductNotFoundException(f"Product '{identifier}' not found.")
        return product

    async def list_categories(self) -> List[Category]:
        return await self.product_repo.list_categories()

    async def list_brands(self) -> List[Brand]:
        return await self.product_repo.list_brands()

    async def list_promotions(self) -> List[Promotion]:
        return await self.product_repo.list_promotions()
