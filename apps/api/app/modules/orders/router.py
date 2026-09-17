import uuid
import random
import logging
from datetime import datetime
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Order, OrderItem, Product
from app.schemas import OrderCheckoutRequest, OrderResponse, OrderItemResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["Orders"])

def generate_order_number() -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    rand_suffix = random.randint(1000, 9999)
    return f"ORD-{timestamp}-{rand_suffix}"

@router.post("", response_model=OrderResponse)
@router.post("/checkout", response_model=OrderResponse)
async def checkout_order(
    body: OrderCheckoutRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Creates an order in PENDING_PAYMENT state from customer cart and configuration selections.
    """
    if not body.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )

    # Calculate subtotal and verify products
    calculated_subtotal = 0.0
    order_items_to_create = []

    for item in body.items:
        item_total = item.unit_price * item.quantity
        calculated_subtotal += item_total
        order_items_to_create.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item_total,
            "configuration_snapshot": item.configuration_snapshot or {},
            "product_title": item.product_title
        })

    total_amount = max(0.0, calculated_subtotal + body.shipping_fee - body.discount_amount)
    order_number = generate_order_number()

    new_order = Order(
        order_number=order_number,
        customer_name=body.customer_name,
        customer_email=body.customer_email,
        customer_phone=body.customer_phone or body.shipping_address.phone_number,
        shipping_address=body.shipping_address.model_dump(),
        status="PENDING_PAYMENT",
        subtotal=calculated_subtotal,
        shipping_fee=body.shipping_fee,
        discount_amount=body.discount_amount,
        total_amount=total_amount,
        currency="NGN"
    )

    db.add(new_order)
    await db.flush()

    for item_dict in order_items_to_create:
        db_item = OrderItem(
            order_id=new_order.id,
            product_id=item_dict["product_id"],
            quantity=item_dict["quantity"],
            unit_price=item_dict["unit_price"],
            total_price=item_dict["total_price"],
            configuration_snapshot=item_dict["configuration_snapshot"]
        )
        db.add(db_item)

    await db.commit()
    await db.refresh(new_order)

    # Reload with items
    stmt = select(Order).options(selectinload(Order.items)).where(Order.id == new_order.id)
    res = await db.execute(stmt)
    full_order = res.scalar_one()

    return OrderResponse(
        id=full_order.id,
        order_number=full_order.order_number,
        customer_name=full_order.customer_name,
        customer_email=full_order.customer_email,
        customer_phone=full_order.customer_phone,
        shipping_address=full_order.shipping_address,
        status=full_order.status,
        subtotal=full_order.subtotal,
        shipping_fee=full_order.shipping_fee,
        discount_amount=full_order.discount_amount,
        total_amount=full_order.total_amount,
        currency=full_order.currency,
        created_at=full_order.created_at.isoformat() if full_order.created_at else None,
        items=[
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
                configuration_snapshot=item.configuration_snapshot
            )
            for item in full_order.items
        ]
    )

@router.get("", response_model=List[OrderResponse])
async def list_orders(
    customer_email: Optional[str] = Query(None, description="Filter by customer email"),
    status: Optional[str] = Query(None, description="Filter by order status"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Lists orders with optional filtering by customer email or order status.
    """
    stmt = select(Order).options(selectinload(Order.items))
    if customer_email:
        stmt = stmt.where(Order.customer_email.ilike(customer_email.strip()))
    if status:
        stmt = stmt.where(Order.status == status)

    stmt = stmt.order_by(Order.created_at.desc()).offset((page - 1) * limit).limit(limit)
    res = await db.execute(stmt)
    orders = res.scalars().all()

    return [
        OrderResponse(
            id=o.id,
            order_number=o.order_number,
            customer_name=o.customer_name,
            customer_email=o.customer_email,
            customer_phone=o.customer_phone,
            shipping_address=o.shipping_address,
            status=o.status,
            subtotal=o.subtotal,
            shipping_fee=o.shipping_fee,
            discount_amount=o.discount_amount,
            total_amount=o.total_amount,
            currency=o.currency,
            payment_reference=o.payment_reference,
            payment_gateway=o.payment_gateway,
            paid_at=o.paid_at.isoformat() if o.paid_at else None,
            created_at=o.created_at.isoformat() if o.created_at else None,
            items=[
                OrderItemResponse(
                    id=item.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price,
                    configuration_snapshot=item.configuration_snapshot
                )
                for item in o.items
            ]
        )
        for o in orders
    ]

@router.get("/{id}", response_model=OrderResponse)
async def get_order_by_id_or_number(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves full order details and current build/delivery status by UUID or order number.
    """
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(or_(Order.id == id, Order.order_number == id))
    )
    res = await db.execute(stmt)
    order = res.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{id}' not found")

    return OrderResponse(
        id=order.id,
        order_number=order.order_number,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,
        status=order.status,
        subtotal=order.subtotal,
        shipping_fee=order.shipping_fee,
        discount_amount=order.discount_amount,
        total_amount=order.total_amount,
        currency=order.currency,
        payment_reference=order.payment_reference,
        payment_gateway=order.payment_gateway,
        paid_at=order.paid_at.isoformat() if order.paid_at else None,
        created_at=order.created_at.isoformat() if order.created_at else None,
        items=[
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
                configuration_snapshot=item.configuration_snapshot
            )
            for item in order.items
        ]
    )
