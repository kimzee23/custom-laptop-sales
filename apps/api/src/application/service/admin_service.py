import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from src.domain.model.order import Order
from src.domain.model.product import Product
from src.domain.model.user import User
from src.domain.exception.exceptions import ProductNotFoundException
from src.application.ports.inbound.admin_usecase import AdminUseCase
from src.application.ports.outbound.order_repository_port import OrderRepositoryPort
from src.application.ports.outbound.product_repository_port import ProductRepositoryPort
from src.application.ports.outbound.user_repository_port import UserRepositoryPort

class AdminService(AdminUseCase):
    def __init__(
        self,
        order_repo: OrderRepositoryPort,
        product_repo: ProductRepositoryPort,
        user_repo: UserRepositoryPort
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.user_repo = user_repo

    async def get_dashboard_summary(self) -> Dict[str, Any]:
        orders = await self.order_repo.list_orders(limit=500)
        users = await self.user_repo.list_users(limit=500)
        products = await self.product_repo.list_products(limit=500)

        total_revenue = sum(o.total_amount for o in orders)
        return {
            "total_revenue": total_revenue,
            "total_orders": len(orders),
            "total_customers": len(users),
            "total_products": len(products),
            "recent_orders": [
                {
                    "id": o.id,
                    "order_number": o.order_number,
                    "customer_name": o.customer_name,
                    "total_amount": o.total_amount,
                    "status": o.status.value if hasattr(o.status, "value") else str(o.status),
                    "created_at": o.created_at.isoformat() if o.created_at else None
                }
                for o in orders[:5]
            ]
        }

    async def list_all_orders(self, status: Optional[str] = None, page: int = 1, page_size: int = 50) -> List[Order]:
        skip = (page - 1) * page_size
        return await self.order_repo.list_orders(status=status, skip=skip, limit=page_size)

    async def list_all_customers(self, page: int = 1, page_size: int = 50) -> List[User]:
        skip = (page - 1) * page_size
        return await self.user_repo.list_users(skip=skip, limit=page_size)

    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        new_prod = Product(
            id=str(uuid.uuid4()),
            title=product_data["title"],
            slug=product_data["slug"],
            description=product_data.get("description"),
            short_description=product_data.get("short_description"),
            category_id=product_data.get("category_id"),
            brand_id=product_data.get("brand_id"),
            base_price=float(product_data.get("base_price", 0.0)),
            original_price=float(product_data["original_price"]) if product_data.get("original_price") else None,
            discount_percentage=product_data.get("discount_percentage"),
            is_featured=product_data.get("is_featured", False),
            is_flash_deal=product_data.get("is_flash_deal", False),
            is_best_seller=product_data.get("is_best_seller", False),
            is_customizable=product_data.get("is_customizable", True),
            stock=product_data.get("stock", 10),
            image_url=product_data.get("image_url", ""),
            gallery_images=product_data.get("gallery_images", []),
            specs=product_data.get("specs", {}),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        return await self.product_repo.save_product(new_prod)

    async def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Product:
        prod = await self.product_repo.get_by_id(product_id)
        if not prod:
            raise ProductNotFoundException(f"Product {product_id} not found.")

        for key, val in product_data.items():
            if hasattr(prod, key) and val is not None:
                setattr(prod, key, val)
        prod.updated_at = datetime.now(timezone.utc)
        return await self.product_repo.save_product(prod)

    async def delete_product(self, product_id: str) -> bool:
        return await self.product_repo.delete_product(product_id)
