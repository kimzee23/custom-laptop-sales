import uuid
from fastapi import APIRouter, Depends, Path, Query, status
from typing import Optional, List
from src.domain.model.order import OrderStatus
from src.application.service.admin_service import AdminService
from src.application.service.product_service import ProductService
from src.application.service.configuration_service import ConfigurationService
from src.application.service.order_service import OrderService
from src.infrastructure.adapters.inbound.rest.dependencies import (
    get_admin_service, get_product_service, get_configuration_service, get_order_service,
    get_current_admin
)
from src.infrastructure.adapters.inbound.rest.dtos.schemas import (
    ProductCreateRequest, ProductUpdateRequest, ConfigurationOptionCreateRequest,
    OrderStatusUpdateRequest
)
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/analytics")
async def get_admin_analytics(
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(get_current_admin)
):
    return await admin_service.get_dashboard_summary()

@router.get("/products")
async def get_admin_products(
    product_service: ProductService = Depends(get_product_service),
    current_admin = Depends(get_current_admin)
):
    prods = await product_service.list_products(page=1, page_size=100)
    return [
        {
            "id": product.id,
            "title": product.title,
            "slug": product.slug,
            "base_price": product.base_price,
            "stock": product.stock,
            "is_featured": product.is_featured,
            "category": product.category.name if product.category else None,
            "brand": product.brand.name if product.brand else None
        }
        for product in prods
    ]

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(
    req: ProductCreateRequest,
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(get_current_admin)
):
    prod = await admin_service.create_product(req.model_dump())
    return {
        "id": prod.id,
        "title": prod.title,
        "slug": prod.slug,
        "base_price": prod.base_price,
        "stock": prod.stock,
        "message": "Product created successfully."
    }

@router.patch("/products/{product_id}")
async def update_product(
    product_id: str = Path(...),
    req: ProductUpdateRequest = ...,
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(get_current_admin)
):
    updated = await admin_service.update_product(product_id, req.model_dump(exclude_unset=True))
    return {
        "id": updated.id,
        "title": updated.title,
        "stock": updated.stock,
        "base_price": updated.base_price,
        "message": "Product updated successfully."
    }

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str = Path(...),
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(get_current_admin)
):
    success = await admin_service.delete_product(product_id)
    return {"success": success, "message": "Product deleted successfully."}

@router.get("/configurations")
async def get_admin_configurations(
    config_service: ConfigurationService = Depends(get_configuration_service),
    current_admin = Depends(get_current_admin)
):
    cats = await config_service.get_configuration_categories()
    return [
        {
            "id": admin_configuration.id,
            "code": admin_configuration.code,
            "name": admin_configuration.name,
            "options_count": len(admin_configuration.options),
            "options": [
                {
                    "id": opt.id,
                    "code": opt.code,
                    "name": opt.name,
                    "price_modifier": opt.price_modifier,
                    "stock": opt.stock
                }
                for opt in admin_configuration.options
            ]
        }
        for admin_configuration in cats
    ]

@router.post("/configurations", status_code=status.HTTP_201_CREATED)
async def add_configuration_option(
    req: ConfigurationOptionCreateRequest,
    config_service: ConfigurationService = Depends(get_configuration_service),
    current_admin = Depends(get_current_admin)
):
    category_id = req.category_id
    if not category_id and req.category_code:
        cats = await config_service.get_configuration_categories()
        for c in cats:
            if c.code.lower() == req.category_code.lower():
                category_id = c.id
                break
    category_id = category_id or "cat-ram"

    from src.domain.model.configuration import ConfigurationOption
    opt = ConfigurationOption(
        id=str(uuid.uuid4()),
        category_id=category_id,
        code=req.code,
        name=req.name,
        price_modifier=req.price_modifier,
        stock=req.stock,
        is_active=True,
        display_order=req.display_order,
        metadata_json=req.metadata_json
    )
    saved = await config_service.config_repo.add_configuration_option(opt)
    return {
        "id": saved.id,
        "name": saved.name,
        "code": saved.code,
        "price_modifier": saved.price_modifier,
        "message": "Configuration option created successfully."
    }

@router.get("/orders")
async def get_admin_orders(
    status: Optional[str] = Query(None),
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(get_current_admin)
):
    orders = await admin_service.list_all_orders(status=status)
    return [
        {
            "id": order.id,
            "order_number": order.order_number,
            "customer_name": order.customer_name,
            "customer_email": order.customer_email,
            "total_amount": order.total_amount,
            "status": order.status.value if hasattr(order.status, "value") else str(order.status),
            "created_at": order.created_at.isoformat() if order.created_at else None
        }
        for order in orders
    ]

@router.patch("/orders/{order_id}")
async def update_order_status(
    order_id: str = Path(...),
    req: OrderStatusUpdateRequest = ...,
    order_service: OrderService = Depends(get_order_service),
    current_admin = Depends(get_current_admin)
):
    status_enum = OrderStatus(req.status.upper())
    updated = await order_service.update_order_status(order_id, status_enum)
    return {
        "id": updated.id,
        "order_number": updated.order_number,
        "status": updated.status.value,
        "message": f"Order status updated to {updated.status.value}."
    }

@router.get("/customers")
async def get_admin_customers(
    admin_service: AdminService = Depends(get_admin_service),
    current_admin = Depends(get_current_admin)
):
    customers = await admin_service.list_all_customers()
    return [
        {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "role": customer.role,
            "reward_points": customer.reward_points
        }
        for customer in customers
    ]
