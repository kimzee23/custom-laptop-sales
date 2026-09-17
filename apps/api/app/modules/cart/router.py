import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Cart, CartItem, Product
from app.schemas import (
    CartResponse,
    CartItemResponse,
    CartItemCreateRequest,
    CartItemUpdateRequest
)
from app.seed_data import PRODUCTS_DATA

router = APIRouter(prefix="/cart", tags=["Cart"])

async def get_or_create_cart(
    session_id: Optional[str],
    user_id: Optional[str],
    db: AsyncSession
) -> Cart:
    effective_session_id = session_id or "default-session"
    stmt = (
        select(Cart)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
        .where(
            (Cart.user_id == user_id) if user_id else (Cart.session_id == effective_session_id)
        )
    )
    res = await db.execute(stmt)
    cart = res.scalars().first()
    
    if not cart:
        cart = Cart(
            id=str(uuid.uuid4()),
            session_id=effective_session_id,
            user_id=user_id
        )
        db.add(cart)
        await db.commit()
        await db.refresh(cart)
        
        stmt = select(Cart).options(selectinload(Cart.items)).where(Cart.id == cart.id)
        res = await db.execute(stmt)
        cart = res.scalars().first()
        
    return cart

async def build_cart_response(cart_id: str, db: AsyncSession) -> CartResponse:
    stmt = (
        select(CartItem)
        .options(selectinload(CartItem.product))
        .where(CartItem.cart_id == cart_id)
    )
    res = await db.execute(stmt)
    cart_items = res.scalars().all()

    items = []
    subtotal = 0.0

    for item in cart_items:
        prod_title = item.product.title if item.product else "Custom Laptop"
        img_url = (
            item.product.image_url 
            if item.product and item.product.image_url 
            else "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80"
        )
        items.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_title=prod_title,
            image_url=img_url,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price,
            configuration_summary=item.configuration_data or {}
        ))
        subtotal += item.total_price

    shipping = 0.0
    discount = 0.0
    total = max(0.0, subtotal + shipping - discount)

    return CartResponse(
        items=items,
        subtotal=subtotal,
        discount=discount,
        shipping=shipping,
        total=total,
        currency="NGN"
    )

@router.get("", response_model=CartResponse)
async def get_cart(
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),
    session_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves the customer's current shopping cart and price calculation.
    """
    effective_session = x_session_id or session_id or "guest-session"
    cart = await get_or_create_cart(effective_session, user_id, db)
    return await build_cart_response(cart.id, db)

@router.post("/items", response_model=CartResponse)
async def add_item_to_cart(
    body: CartItemCreateRequest,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),
    session_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Adds a laptop or custom-configured item to the cart.
    """
    effective_session = x_session_id or session_id or "guest-session"
    cart = await get_or_create_cart(effective_session, user_id, db)

    # Determine unit price
    unit_price = body.unit_price
    if unit_price is None:
        p_res = await db.execute(select(Product).where(Product.id == body.product_id))
        prod = p_res.scalars().first()
        if prod:
            unit_price = prod.base_price
        else:
            for p in PRODUCTS_DATA:
                if p["id"] == body.product_id or p["slug"] == body.product_id:
                    unit_price = p["base_price"]
                    break
            if unit_price is None:
                unit_price = 850000.0

    total_price = unit_price * body.quantity

    new_item = CartItem(
        id=str(uuid.uuid4()),
        cart_id=cart.id,
        product_id=body.product_id,
        quantity=body.quantity,
        unit_price=unit_price,
        total_price=total_price,
        configuration_data=body.configuration_data or {}
    )
    db.add(new_item)
    await db.commit()

    return await build_cart_response(cart.id, db)

@router.patch("/items/{id}", response_model=CartResponse)
async def update_cart_item(
    id: str,
    body: CartItemUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Updates quantity of an item in the cart.
    """
    item_res = await db.execute(select(CartItem).where(CartItem.id == id))
    item = item_res.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    item.quantity = body.quantity
    item.total_price = item.unit_price * body.quantity
    await db.commit()

    return await build_cart_response(item.cart_id, db)

@router.delete("/items/{id}", response_model=CartResponse)
async def delete_cart_item(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Removes an item from the cart.
    """
    item_res = await db.execute(select(CartItem).where(CartItem.id == id))
    item = item_res.scalars().first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    cart_id = item.cart_id
    await db.delete(item)
    await db.commit()

    return await build_cart_response(cart_id, db)
