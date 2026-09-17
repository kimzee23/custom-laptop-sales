from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models import Product, Category, Brand, Review, Promotion
from app.schemas import ProductResponse, CategoryResponse, BrandResponse, ReviewResponse, PromotionResponse
from app.seed_data import PRODUCTS_DATA, CATEGORIES_DATA, BRANDS_DATA, PROMOTIONS_DATA

router = APIRouter(prefix="", tags=["Products & Catalog"])

@router.get("/promotions", response_model=List[PromotionResponse])
async def list_promotions(db: AsyncSession = Depends(get_db)):
    """
    Returns active promotions, banners, and coupon codes for laptop builds.
    """
    try:
        result = await db.execute(select(Promotion).where(Promotion.is_active == True))
        promos = result.scalars().all()
        if not promos:
            return [PromotionResponse(**p) for p in PROMOTIONS_DATA]
        return promos
    except Exception:
        return [PromotionResponse(**p) for p in PROMOTIONS_DATA]

@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.display_order))
    categories = result.scalars().all()
    if not categories:
        # Fallback to in-memory seed if DB hasn't been initialized yet
        return [CategoryResponse(**c) for c in CATEGORIES_DATA]
    return categories

@router.get("/brands", response_model=List[BrandResponse])
async def list_brands(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand))
    brands = result.scalars().all()
    if not brands:
        return [BrandResponse(**b) for b in BRANDS_DATA]
    return brands

@router.get("/products", response_model=List[ProductResponse])
async def list_products(
    category_id: Optional[str] = None,
    brand_id: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_featured: Optional[bool] = None,
    is_flash_deal: Optional[bool] = None,
    is_best_seller: Optional[bool] = None,
    sort: Optional[str] = Query(None, description="price_asc, price_desc, rating, newest"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(Product).options(selectinload(Product.category), selectinload(Product.brand))
        conditions = []
        
        if category_id:
            conditions.append(Product.category_id == category_id)
        if brand_id:
            conditions.append(Product.brand_id == brand_id)
        if search:
            search_pattern = f"%{search}%"
            conditions.append(or_(
                Product.title.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.short_description.ilike(search_pattern)
            ))
        if min_price is not None:
            conditions.append(Product.base_price >= min_price)
        if max_price is not None:
            conditions.append(Product.base_price <= max_price)
        if is_featured is not None:
            conditions.append(Product.is_featured == is_featured)
        if is_flash_deal is not None:
            conditions.append(Product.is_flash_deal == is_flash_deal)
        if is_best_seller is not None:
            conditions.append(Product.is_best_seller == is_best_seller)
            
        if conditions:
            query = query.where(and_(*conditions))
            
        if sort == "price_asc":
            query = query.order_by(Product.base_price.asc())
        elif sort == "price_desc":
            query = query.order_by(Product.base_price.desc())
        elif sort == "rating":
            query = query.order_by(Product.rating.desc())
        else:
            query = query.order_by(Product.created_at.desc())
            
        query = query.offset((page - 1) * limit).limit(limit)
            
        result = await db.execute(query)
        products = result.scalars().all()
        if not products and not category_id and not search:
            return [ProductResponse(**p) for p in PRODUCTS_DATA]
        return products
    except Exception:
        return [ProductResponse(**p) for p in PRODUCTS_DATA]

@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.product_id == product_id))
    return result.scalars().all()

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category), selectinload(Product.brand))
        .where(or_(Product.id == product_id, Product.slug == product_id))
    )
    product = result.scalars().first()
    if not product:
        for p in PRODUCTS_DATA:
            if p["id"] == product_id or p["slug"] == product_id:
                return ProductResponse(**p)
        raise HTTPException(status_code=404, detail="Product not found")
    return product
