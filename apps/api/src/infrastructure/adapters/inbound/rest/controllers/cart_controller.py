from fastapi import APIRouter, Depends, Query, Header, Path, status
from typing import Optional
from src.application.service.cart_service import CartService
from src.infrastructure.adapters.inbound.rest.dependencies import (
    get_cart_service, get_optional_user
)
from src.infrastructure.adapters.inbound.rest.dtos.schemas import (
    CartItemAddRequest, CartItemUpdateRequest
)

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

def _cart_to_dict(cart):
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "session_id": cart.session_id,
        "subtotal": cart.subtotal,
        "total_items": cart.total_items,
        "items": [
            {
                "id": it.id,
                "product_id": it.product_id,
                "quantity": it.quantity,
                "unit_price": it.unit_price,
                "total_price": it.total_price,
                "configuration_data": it.configuration_data,
                "product_title": it.product_title,
                "product_image": it.product_image
            }
            for it in cart.items
        ]
    }

@router.get("")
async def get_cart(
    session_id: Optional[str] = Query(None),
    x_session_id: Optional[str] = Header(None),
    user = Depends(get_optional_user),
    cart_service: CartService = Depends(get_cart_service)
):
    sid = session_id or x_session_id or "default-session"
    uid = user.id if user else None
    cart = await cart_service.get_cart(session_id=sid, user_id=uid)
    return _cart_to_dict(cart)

@router.post("/items")
async def add_item_to_cart(
    req: CartItemAddRequest,
    x_session_id: Optional[str] = Header(None),
    user = Depends(get_optional_user),
    cart_service: CartService = Depends(get_cart_service)
):
    sid = req.session_id or x_session_id or "default-session"
    uid = user.id if user else None
    item = await cart_service.add_item(
        session_id=sid,
        user_id=uid,
        product_id=req.product_id,
        quantity=req.quantity,
        unit_price=req.unit_price,
        configuration_data=req.configuration_data
    )
    cart = await cart_service.get_cart(session_id=sid, user_id=uid)
    return _cart_to_dict(cart)

@router.patch("/items/{item_id}")
async def update_cart_item(
    item_id: str = Path(...),
    req: CartItemUpdateRequest = ...,
    x_session_id: Optional[str] = Header(None),
    user = Depends(get_optional_user),
    cart_service: CartService = Depends(get_cart_service)
):
    await cart_service.update_item_quantity(item_id=item_id, quantity=req.quantity)
    sid = x_session_id or "default-session"
    uid = user.id if user else None
    cart = await cart_service.get_cart(session_id=sid, user_id=uid)
    return _cart_to_dict(cart)

@router.delete("/items/{item_id}")
async def remove_cart_item(
    item_id: str = Path(...),
    x_session_id: Optional[str] = Header(None),
    user = Depends(get_optional_user),
    cart_service: CartService = Depends(get_cart_service)
):
    await cart_service.remove_item(item_id=item_id)
    sid = x_session_id or "default-session"
    uid = user.id if user else None
    cart = await cart_service.get_cart(session_id=sid, user_id=uid)
    return _cart_to_dict(cart)

@router.delete("")
async def clear_cart(
    x_session_id: Optional[str] = Header(None),
    user = Depends(get_optional_user),
    cart_service: CartService = Depends(get_cart_service)
):
    sid = x_session_id or "default-session"
    uid = user.id if user else None
    await cart_service.clear_cart(session_id=sid, user_id=uid)
    return {"message": "Cart cleared successfully."}
