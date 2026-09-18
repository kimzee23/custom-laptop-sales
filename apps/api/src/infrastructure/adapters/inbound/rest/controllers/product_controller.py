from fastapi import APIRouter, Depends, Query, Path
from typing import Optional, List
from src.application.service.product_service import ProductService
from src.application.service.configuration_service import ConfigurationService
from src.infrastructure.adapters.inbound.rest.dependencies import (
    get_product_service, get_configuration_service
)
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(tags=["Product Catalog"])

def _product_to_dict(p):
    return {
        "id": p.id,
        "title": p.title,
        "slug": p.slug,
        "description": p.description,
        "short_description": p.short_description,
        "category_id": p.category_id,
        "brand_id": p.brand_id,
        "base_price": p.base_price,
        "original_price": p.original_price,
        "discount_percentage": p.discount_percentage,
        "is_featured": p.is_featured,
        "is_flash_deal": p.is_flash_deal,
        "is_best_seller": p.is_best_seller,
        "is_customizable": p.is_customizable,
        "stock": p.stock,
        "rating": p.rating,
        "review_count": p.review_count,
        "image_url": p.image_url,
        "gallery_images": p.gallery_images,
        "specs": p.specs,
        "model_3d_url": p.model_3d_url,
        "category": {
            "id": p.category.id,
            "name": p.category.name,
            "slug": p.category.slug
        } if p.category else None,
        "brand": {
            "id": p.brand.id,
            "name": p.brand.name,
            "slug": p.brand.slug
        } if p.brand else None
    }

@router.get("/products")
async def list_products(
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    flash_deals: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    product_service: ProductService = Depends(get_product_service)
):
    products = await product_service.list_products(
        category=category,
        brand=brand,
        featured=featured,
        flash_deals=flash_deals,
        search=search,
        sort=sort,
        min_price=min_price,
        max_price=max_price,
        page=page,
        page_size=page_size
    )
    # Return directly list to preserve existing frontend and test compatibility
    return [_product_to_dict(p) for p in products]

@router.get("/products/{identifier}")
async def get_product(
    identifier: str = Path(...),
    product_service: ProductService = Depends(get_product_service)
):
    product = await product_service.get_product_by_id_or_slug(identifier)
    return _product_to_dict(product)

@router.get("/categories")
async def list_categories(product_service: ProductService = Depends(get_product_service)):
    categories = await product_service.list_categories()
    return [
        {
            "id": c.id,
            "name": c.name,
            "slug": c.slug,
            "description": c.description,
            "image_url": c.image_url,
            "icon": c.icon,
            "display_order": c.display_order
        }
        for c in categories
    ]

@router.get("/brands")
async def list_brands(product_service: ProductService = Depends(get_product_service)):
    brands = await product_service.list_brands()
    return [
        {
            "id": b.id,
            "name": b.name,
            "slug": b.slug,
            "logo_url": b.logo_url
        }
        for b in brands
    ]

@router.get("/promotions")
async def list_promotions(product_service: ProductService = Depends(get_product_service)):
    promotions = await product_service.list_promotions()
    return [
        {
            "id": p.id,
            "title": p.title,
            "code": p.code,
            "description": p.description,
            "discount_type": p.discount_type,
            "discount_value": p.discount_value,
            "banner_url": p.banner_url,
            "is_active": p.is_active
        }
        for p in promotions
    ]

@router.get("/products/{identifier}/configurations")
async def get_product_configurations(
    identifier: str = Path(...),
    config_service: ConfigurationService = Depends(get_configuration_service)
):
    cats = await config_service.get_configuration_categories(product_id=identifier)
    return [
        {
            "id": c.id,
            "code": c.code,
            "name": c.name,
            "display_order": c.display_order,
            "is_required": c.is_required,
            "options": [
                {
                    "id": opt.id,
                    "category_id": opt.category_id,
                    "code": opt.code,
                    "name": opt.name,
                    "price_modifier": opt.price_modifier,
                    "stock": opt.stock,
                    "is_active": opt.is_active,
                    "display_order": opt.display_order,
                    "metadata": opt.metadata_json
                }
                for opt in c.options
            ]
        }
        for c in cats
    ]
