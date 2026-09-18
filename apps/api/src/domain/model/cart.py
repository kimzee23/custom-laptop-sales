from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class CartItem:
    id: str
    cart_id: str
    product_id: str
    quantity: int = 1
    unit_price: float = 0.0
    total_price: float = 0.0
    configuration_data: Dict[str, Any] = field(default_factory=dict)
    product_title: Optional[str] = None
    product_image: Optional[str] = None

@dataclass
class Cart:
    id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items: List[CartItem] = field(default_factory=list)

    @property
    def subtotal(self) -> float:
        return sum(item.total_price for item in self.items)

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)
