from fastapi import APIRouter, Depends, Query, Path, status
from typing import Optional, List
from src.application.service.order_service import OrderService
from src.infrastructure.adapters.inbound.rest.dependencies import (
    get_order_service, get_optional_user
)
from src.infrastructure.adapters.inbound.rest.dtos.schemas import OrderCreateRequest
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(prefix="/orders", tags=["Orders & Checkout"])

def _order_to_dict(order):
    return {
        "id": order.id,
        "order_number": order.order_number,
        "user_id": order.user_id,
        "customer_name": order.customer_name,
        "customer_email": order.customer_email,
        "customer_phone": order.customer_phone,
        "shipping_address": order.shipping_address,
        "status": order.status.value if hasattr(order.status, "value") else str(order.status),
        "subtotal": order.subtotal,
        "shipping_fee": order.shipping_fee,
        "discount_amount": order.discount_amount,
        "total_amount": order.total_amount,
        "currency": order.currency,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "updated_at": order.updated_at.isoformat() if order.updated_at else None,
        "paid_at": order.paid_at.isoformat() if order.paid_at else None,
        "payment_reference": order.payment_reference,
        "payment_gateway": order.payment_gateway,
        "items": [
            {
                "id": it.id,
                "product_id": it.product_id,
                "quantity": it.quantity,
                "unit_price": it.unit_price,
                "total_price": it.total_price,
                "configuration_snapshot": it.configuration_snapshot,
                "product_title": it.product_title,
                "product_image": it.product_image
            }
            for it in order.items
        ]
    }

@router.post("")
async def create_order(
    req: OrderCreateRequest,
    user = Depends(get_optional_user),
    order_service: OrderService = Depends(get_order_service)
):
    items_data = [item.model_dump() for item in req.items]
    order = await order_service.create_order(
        customer_name=req.customer_name,
        customer_email=req.customer_email,
        customer_phone=req.customer_phone,
        shipping_address=req.shipping_address,
        items=items_data,
        user_id=user.id if user else None
    )
    return _order_to_dict(order)

@router.get("")
async def list_orders(
    user = Depends(get_optional_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_service: OrderService = Depends(get_order_service)
):
    uid = user.id if user else None
    orders = await order_service.list_orders(user_id=uid, page=page, page_size=page_size)
    return [_order_to_dict(o) for o in orders]

@router.get("/{identifier}")
async def get_order(
    identifier: str = Path(...),
    order_service: OrderService = Depends(get_order_service)
):
    order = await order_service.get_order_by_id_or_number(identifier)
    return _order_to_dict(order)
