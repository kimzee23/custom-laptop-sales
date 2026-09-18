from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

class OrderStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    CUSTOM_BUILD = "CUSTOM_BUILD"
    READY_FOR_SHIPPING = "READY_FOR_SHIPPING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

@dataclass
class OrderItem:
    id: str
    order_id: str
    product_id: str
    quantity: int = 1
    unit_price: float = 0.0
    total_price: float = 0.0
    configuration_snapshot: Dict[str, Any] = field(default_factory=dict)
    product_title: Optional[str] = None
    product_image: Optional[str] = None

@dataclass
class Order:
    id: str
    order_number: str
    customer_name: str
    customer_email: str
    shipping_address: Dict[str, Any]
    subtotal: float
    total_amount: float
    user_id: Optional[str] = None
    customer_phone: Optional[str] = None
    shipping_fee: float = 0.0
    discount_amount: float = 0.0
    currency: str = "NGN"
    status: OrderStatus = OrderStatus.PENDING_PAYMENT
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    payment_reference: Optional[str] = None
    payment_gateway: Optional[str] = None
    items: List[OrderItem] = field(default_factory=list)
