from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# Auth DTOs
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: str
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class CheckUserRequest(BaseModel):
    email: str

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)

class PasswordForgotRequest(BaseModel):
    email: str

class PasswordResetRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

# Product DTOs
class ProductCreateRequest(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    base_price: float
    original_price: Optional[float] = None
    discount_percentage: Optional[int] = None
    is_featured: bool = False
    is_flash_deal: bool = False
    is_best_seller: bool = False
    is_customizable: bool = True
    stock: int = 10
    image_url: str
    gallery_images: List[str] = []
    specs: Dict[str, Any] = {}

class ProductUpdateRequest(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    base_price: Optional[float] = None
    original_price: Optional[float] = None
    discount_percentage: Optional[int] = None
    is_featured: Optional[bool] = None
    is_flash_deal: Optional[bool] = None
    is_best_seller: Optional[bool] = None
    is_customizable: Optional[bool] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    gallery_images: Optional[List[str]] = None
    specs: Optional[Dict[str, Any]] = None

# Configuration DTOs
class PriceCalculationRequest(BaseModel):
    product_id: Optional[str] = None
    color_id: Optional[str] = None
    ram_id: Optional[str] = None
    storage_id: Optional[str] = None
    cpu_id: Optional[str] = None
    gpu_id: Optional[str] = None
    display_id: Optional[str] = None
    keyboard_id: Optional[str] = None
    accessory_ids: Optional[List[str]] = []
    artwork: Optional[Dict[str, Any]] = None
    base_price: Optional[float] = None
    selected_option_ids: Optional[List[str]] = []

class ConfigurationSubmitRequest(BaseModel):
    product_id: str
    color_id: Optional[str] = None
    ram_id: Optional[str] = None
    storage_id: Optional[str] = None
    cpu_id: Optional[str] = None
    gpu_id: Optional[str] = None
    display_id: Optional[str] = None
    keyboard_id: Optional[str] = None
    accessory_ids: Optional[List[str]] = []
    artwork: Optional[Dict[str, Any]] = None
    specs: Optional[Dict[str, Any]] = None
    base_price: Optional[float] = None
    total_price: Optional[float] = None

class SaveBuildRequest(BaseModel):
    title: str
    product_id: str
    image_url: Optional[str] = None
    total_price: float
    configuration_snapshot: Dict[str, Any] = {}
    specs_summary: Dict[str, Any] = {}
    user_id: Optional[str] = None

class ConfigurationOptionCreateRequest(BaseModel):
    category_id: Optional[str] = None
    category_code: Optional[str] = None
    code: str
    name: str
    price_modifier: float = 0.0
    stock: int = 100
    display_order: int = 0
    metadata_json: Dict[str, Any] = {}

# Cart DTOs
class CartItemAddRequest(BaseModel):
    product_id: str
    quantity: int = 1
    unit_price: float
    configuration_data: Dict[str, Any] = {}
    session_id: Optional[str] = None

class CartItemUpdateRequest(BaseModel):
    quantity: int

# Order DTOs
class OrderItemDTO(BaseModel):
    product_id: str
    quantity: int = 1
    unit_price: float
    configuration_snapshot: Dict[str, Any] = {}
    product_title: Optional[str] = None
    product_image: Optional[str] = None

class OrderCreateRequest(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: Dict[str, Any]
    items: List[OrderItemDTO]

class OrderStatusUpdateRequest(BaseModel):
    status: str

# Payment DTOs
class PaymentInitializeRequest(BaseModel):
    order_id: Optional[str] = None
    order_number: Optional[str] = None
    provider: str = "PAYSTACK"
    idempotency_key: str

class PaymentVerifyRequest(BaseModel):
    reference: str
    provider: str = "PAYSTACK"

# Review DTOs
class ReviewCreateRequest(BaseModel):
    product_id: str
    author_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str

# Analytics DTOs
class TrackVisitRequest(BaseModel):
    session_id: Optional[str] = None
    page_path: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
