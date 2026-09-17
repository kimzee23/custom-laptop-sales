from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models import Product, ConfigurationCategory, ConfigurationOption, SavedConfiguration
from app.schemas import (
    ConfigurationCategoryResponse, 
    ConfigurationPriceRequest, 
    ConfigurationPriceResponse, 
    PriceBreakdownItem,
    ConfigurationCreateRequest,
    ConfigurationResponse,
    SavedBuildCreateRequest,
    SavedBuildResponse
)
from app.seed_data import CONFIGURATION_CATEGORIES_DATA, PRODUCTS_DATA

router = APIRouter(prefix="", tags=["Configurations & Pricing"])

@router.get("/products/{product_id}/configurations", response_model=List[ConfigurationCategoryResponse])
async def get_product_configurations(product_id: str, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(ConfigurationCategory)
            .options(selectinload(ConfigurationCategory.options))
            .order_by(ConfigurationCategory.display_order)
        )
        categories = result.scalars().all()
        if not categories:
            return [ConfigurationCategoryResponse(**c) for c in CONFIGURATION_CATEGORIES_DATA]
        return categories
    except Exception:
        return [ConfigurationCategoryResponse(**c) for c in CONFIGURATION_CATEGORIES_DATA]

@router.post("/configurations/price", response_model=ConfigurationPriceResponse)
async def calculate_configuration_price(
    req: ConfigurationPriceRequest,
    db: AsyncSession = Depends(get_db)
):
    # Fetch Base Product
    product_title = "Custom Configured Laptop"
    base_price = 1000000.0

    # Search in DB or fallback seed
    result = await db.execute(select(Product).where(Product.id == req.product_id))
    product = result.scalars().first()
    if product:
        product_title = product.title
        base_price = product.base_price
    else:
        for p in PRODUCTS_DATA:
            if p["id"] == req.product_id or p["slug"] == req.product_id:
                product_title = p["title"]
                base_price = p["base_price"]
                break

    # Build pricing items breakdown
    items: List[PriceBreakdownItem] = []
    
    # Collect option IDs to inspect
    selected_option_ids = [
        req.color_id,
        req.ram_id,
        req.storage_id,
        req.cpu_id,
        req.gpu_id,
        req.display_id,
        req.keyboard_id
    ]
    if req.accessory_ids:
        selected_option_ids.extend(req.accessory_ids)
    
    selected_option_ids = [opt_id for opt_id in selected_option_ids if opt_id]

    # Map options from DB or fallback
    all_options = {}
    for cat in CONFIGURATION_CATEGORIES_DATA:
        for opt in cat.get("options", []):
            all_options[opt["id"]] = (opt["name"], cat["name"], opt["price_modifier"])
            all_options[opt["code"]] = (opt["name"], cat["name"], opt["price_modifier"])

    # Query DB options if available
    if selected_option_ids:
        try:
            db_opts = await db.execute(
                select(ConfigurationOption)
                .options(selectinload(ConfigurationOption.category))
                .where(ConfigurationOption.id.in_(selected_option_ids))
            )
            for opt in db_opts.scalars().all():
                all_options[opt.id] = (
                    opt.name,
                    opt.category.name if opt.category else "Component",
                    opt.price_modifier
                )
        except Exception:
            pass

    modifiers_total = 0.0
    for opt_id in selected_option_ids:
        if opt_id in all_options:
            name, cat_name, modifier = all_options[opt_id]
            if modifier != 0:
                items.append(PriceBreakdownItem(
                    name=name,
                    category=cat_name,
                    modifier=modifier
                ))
            modifiers_total += modifier

    # Handle Custom Artwork
    artwork_price = 0.0
    if req.artwork and (req.artwork.image_url or req.artwork.custom_text):
        artwork_price = 35000.0
        items.append(PriceBreakdownItem(
            name="Custom Precision UV Artwork / Text Engraving",
            category="Artwork",
            modifier=artwork_price
        ))

    subtotal = base_price + modifiers_total + artwork_price
    shipping = 0.0 # Free shipping threshold
    discount = 0.0
    total = subtotal + shipping - discount

    return ConfigurationPriceResponse(
        product_id=req.product_id,
        product_title=product_title,
        base_price=base_price,
        items=items,
        subtotal=subtotal,
        shipping=shipping,
        discount=discount,
        total=total,
        currency="NGN",
        currency_symbol="₦"
    )

@router.post("/configurations", response_model=ConfigurationResponse)
async def create_custom_configuration(
    req: ConfigurationCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Validates components and builds a custom laptop configuration snapshot with dynamic pricing.
    """
    price_calc = await calculate_configuration_price(
        ConfigurationPriceRequest(
            product_id=req.product_id,
            color_id=req.color_id,
            ram_id=req.ram_id,
            storage_id=req.storage_id,
            cpu_id=req.cpu_id,
            gpu_id=req.gpu_id,
            display_id=req.display_id,
            keyboard_id=req.keyboard_id,
            accessory_ids=req.accessory_ids,
            artwork=req.artwork
        ),
        db=db
    )

    specs_summary = {
        "color": req.color_id,
        "ram": req.ram_id,
        "storage": req.storage_id,
        "cpu": req.cpu_id,
        "gpu": req.gpu_id,
        "display": req.display_id,
        "keyboard": req.keyboard_id,
        "accessories": req.accessory_ids,
        "has_artwork": bool(req.artwork and (req.artwork.image_url or req.artwork.custom_text))
    }

    return ConfigurationResponse(
        product_id=req.product_id,
        product_title=price_calc.product_title,
        base_price=price_calc.base_price,
        total_price=price_calc.total,
        price_breakdown=price_calc.items,
        configuration_snapshot=req.model_dump(),
        specs_summary=specs_summary
    )

@router.get("/saved-builds", response_model=List[SavedBuildResponse])
async def list_saved_builds(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    Lists saved custom 3D laptop builds.
    """
    try:
        query = select(SavedConfiguration)
        if user_id:
            query = query.where(SavedConfiguration.user_id == user_id)
        result = await db.execute(query.order_by(SavedConfiguration.created_at.desc()))
        builds = result.scalars().all()
        return [
            SavedBuildResponse(
                id=b.id,
                user_id=b.user_id,
                title=b.title,
                product_id=b.product_id,
                image_url=b.image_url,
                total_price=b.total_price,
                configuration_snapshot=b.configuration_snapshot or {},
                specs_summary=b.specs_summary or {},
                created_at=b.created_at.isoformat() if b.created_at else None
            )
            for b in builds
        ]
    except Exception:
        return []

@router.post("/saved-builds", response_model=SavedBuildResponse)
async def create_saved_build(
    body: SavedBuildCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Persists a custom laptop build so it can be re-opened, modified, or shared.
    """
    new_build = SavedConfiguration(
        user_id=body.user_id or "guest-user",
        title=body.title,
        product_id=body.product_id,
        image_url=body.image_url or "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80",
        total_price=body.total_price,
        configuration_snapshot=body.configuration_snapshot,
        specs_summary=body.specs_summary or {}
    )
    db.add(new_build)
    await db.commit()
    await db.refresh(new_build)

    return SavedBuildResponse(
        id=new_build.id,
        user_id=new_build.user_id,
        title=new_build.title,
        product_id=new_build.product_id,
        image_url=new_build.image_url,
        total_price=new_build.total_price,
        configuration_snapshot=new_build.configuration_snapshot or {},
        specs_summary=new_build.specs_summary or {},
        created_at=new_build.created_at.isoformat() if new_build.created_at else None
    )
