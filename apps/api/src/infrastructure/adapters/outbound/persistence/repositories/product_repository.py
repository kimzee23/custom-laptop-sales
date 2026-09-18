from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, desc, asc
from sqlalchemy.orm import selectinload
from src.domain.model.product import Product, Category, Brand, Promotion
from src.application.ports.outbound.product_repository_port import ProductRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import (
    ProductEntity, CategoryEntity, BrandEntity, PromotionEntity
)

class ProductRepository(ProductRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, entity: ProductEntity) -> Product:
        category = None
        if hasattr(entity, "category") and entity.category:
            category = Category(
                id=entity.category.id,
                name=entity.category.name,
                slug=entity.category.slug,
                description=entity.category.description,
                image_url=entity.category.image_url,
                icon=entity.category.icon,
                display_order=entity.category.display_order,
                created_at=entity.category.created_at
            )
        brand = None
        if hasattr(entity, "brand") and entity.brand:
            brand = Brand(
                id=entity.brand.id,
                name=entity.brand.name,
                slug=entity.brand.slug,
                logo_url=entity.brand.logo_url
            )

        return Product(
            id=entity.id,
            title=entity.title,
            slug=entity.slug,
            description=entity.description,
            short_description=entity.short_description,
            category_id=entity.category_id,
            brand_id=entity.brand_id,
            base_price=entity.base_price,
            original_price=entity.original_price,
            discount_percentage=entity.discount_percentage,
            is_featured=entity.is_featured,
            is_flash_deal=entity.is_flash_deal,
            is_best_seller=entity.is_best_seller,
            is_customizable=entity.is_customizable,
            stock=entity.stock,
            rating=entity.rating,
            review_count=entity.review_count,
            image_url=entity.image_url,
            gallery_images=entity.gallery_images or [],
            specs=entity.specs or {},
            model_3d_url=entity.model_3d_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            category=category,
            brand=brand
        )

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
        stmt = select(ProductEntity).options(
            selectinload(ProductEntity.category),
            selectinload(ProductEntity.brand)
        )

        if category:
            stmt = stmt.join(ProductEntity.category).where(
                or_(CategoryEntity.slug == category, CategoryEntity.id == category)
            )
        if brand:
            stmt = stmt.join(ProductEntity.brand).where(
                or_(BrandEntity.slug == brand, BrandEntity.id == brand)
            )
        if featured is not None:
            stmt = stmt.where(ProductEntity.is_featured == featured)
        if flash_deals is not None:
            stmt = stmt.where(ProductEntity.is_flash_deal == flash_deals)
        if min_price is not None:
            stmt = stmt.where(ProductEntity.base_price >= min_price)
        if max_price is not None:
            stmt = stmt.where(ProductEntity.base_price <= max_price)
        if search:
            search_term = f"%{search}%"
            stmt = stmt.where(
                or_(
                    ProductEntity.title.ilike(search_term),
                    ProductEntity.description.ilike(search_term),
                    ProductEntity.short_description.ilike(search_term)
                )
            )

        if sort == "price_asc":
            stmt = stmt.order_by(asc(ProductEntity.base_price))
        elif sort == "price_desc":
            stmt = stmt.order_by(desc(ProductEntity.base_price))
        elif sort == "rating":
            stmt = stmt.order_by(desc(ProductEntity.rating))
        else:
            stmt = stmt.order_by(desc(ProductEntity.created_at))

        stmt = stmt.offset(skip).limit(limit)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [self._to_domain(e) for e in entities]

    async def get_by_id(self, product_id: str) -> Optional[Product]:
        stmt = select(ProductEntity).options(
            selectinload(ProductEntity.category),
            selectinload(ProductEntity.brand)
        ).where(ProductEntity.id == product_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        stmt = select(ProductEntity).options(
            selectinload(ProductEntity.category),
            selectinload(ProductEntity.brand)
        ).where(ProductEntity.slug == slug)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def save_product(self, product: Product) -> Product:
        stmt = select(ProductEntity).where(ProductEntity.id == product.id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if not entity:
            entity = ProductEntity(
                id=product.id,
                title=product.title,
                slug=product.slug,
                description=product.description,
                short_description=product.short_description,
                category_id=product.category_id,
                brand_id=product.brand_id,
                base_price=product.base_price,
                original_price=product.original_price,
                discount_percentage=product.discount_percentage,
                is_featured=product.is_featured,
                is_flash_deal=product.is_flash_deal,
                is_best_seller=product.is_best_seller,
                is_customizable=product.is_customizable,
                stock=product.stock,
                image_url=product.image_url,
                gallery_images=product.gallery_images,
                specs=product.specs,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
            self.session.add(entity)
        else:
            entity.title = product.title
            entity.slug = product.slug
            entity.description = product.description
            entity.short_description = product.short_description
            entity.category_id = product.category_id
            entity.brand_id = product.brand_id
            entity.base_price = product.base_price
            entity.original_price = product.original_price
            entity.discount_percentage = product.discount_percentage
            entity.is_featured = product.is_featured
            entity.is_flash_deal = product.is_flash_deal
            entity.is_best_seller = product.is_best_seller
            entity.is_customizable = product.is_customizable
            entity.stock = product.stock
            entity.image_url = product.image_url
            entity.gallery_images = product.gallery_images
            entity.specs = product.specs
            entity.updated_at = product.updated_at

        await self.session.commit()
        await self.session.refresh(entity)
        return self._to_domain(entity)

    async def delete_product(self, product_id: str) -> bool:
        stmt = select(ProductEntity).where(ProductEntity.id == product_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if entity:
            await self.session.delete(entity)
            await self.session.commit()
            return True
        return False

    async def list_categories(self) -> List[Category]:
        stmt = select(CategoryEntity).order_by(CategoryEntity.display_order)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            Category(
                id=c.id,
                name=c.name,
                slug=c.slug,
                description=c.description,
                image_url=c.image_url,
                icon=c.icon,
                display_order=c.display_order,
                created_at=c.created_at
            )
            for c in entities
        ]

    async def list_brands(self) -> List[Brand]:
        stmt = select(BrandEntity).order_by(BrandEntity.name)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            Brand(id=b.id, name=b.name, slug=b.slug, logo_url=b.logo_url)
            for b in entities
        ]

    async def list_promotions(self) -> List[Promotion]:
        stmt = select(PromotionEntity).where(PromotionEntity.is_active == True)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            Promotion(
                id=p.id,
                title=p.title,
                code=p.code,
                description=p.description,
                discount_type=p.discount_type,
                discount_value=p.discount_value,
                banner_url=p.banner_url,
                is_active=p.is_active,
                start_date=p.start_date,
                end_date=p.end_date,
                created_at=p.created_at
            )
            for p in entities
        ]
