from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# -----------------
# Categories & Brands
# -----------------
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0

class CategoryResponse(CategoryBase):
    id: str
    product_count: Optional[int] = 0

    class Config:
        from_attributes = True

class BrandResponse(BaseModel):
    id: str
    name: str
    slug: str
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True

# -----------------
# Configuration Options
# -----------------
class ConfigurationOptionResponse(BaseModel):
    id: str
    code: str
    name: str
    price_modifier: float
    stock: int
    is_active: bool
    display_order: int
    metadata_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ConfigurationCategoryResponse(BaseModel):
    id: str
    code: str
    name: str
    display_order: int
    is_required: bool
    options: List[ConfigurationOptionResponse] = []

    class Config:
        from_attributes = True

# -----------------
# Products
# -----------------
class ProductBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    base_price: float
    original_price: Optional[float] = None
    discount_percentage: Optional[int] = None
    is_featured: bool = False
    is_flash_deal: bool = False
    is_best_seller: bool = False
    is_customizable: bool = True
    stock: int = 10
    rating: float = 4.8
    review_count: int = 0
    image_url: str
    gallery_images: List[str] = []
    specs: Dict[str, Any] = {}
    model_3d_url: Optional[str] = None

class ProductResponse(ProductBase):
    id: str
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None

    class Config:
        from_attributes = True

# -----------------
# Configuration Price Calculation
# -----------------
class ArtworkConfig(BaseModel):
    image_url: Optional[str] = None
    position_x: float = 0.0
    position_y: float = 0.0
    scale: float = 1.0
    rotation: float = 0.0
    custom_text: Optional[str] = None

class ConfigurationPriceRequest(BaseModel):
    product_id: str
    color_id: Optional[str] = None
    ram_id: Optional[str] = None
    storage_id: Optional[str] = None
    cpu_id: Optional[str] = None
    gpu_id: Optional[str] = None
    display_id: Optional[str] = None
    keyboard_id: Optional[str] = None
    accessory_ids: List[str] = []
    artwork: Optional[ArtworkConfig] = None

class PriceBreakdownItem(BaseModel):
    name: str
    category: str
    modifier: float

class ConfigurationPriceResponse(BaseModel):
    product_id: str
    product_title: str
    base_price: float
    items: List[PriceBreakdownItem] = []
    subtotal: float
    shipping: float = 0.0
    discount: float = 0.0
    total: float
    currency: str = "NGN"
    currency_symbol: str = "₦"

# -----------------
# Cart & Checkout
# -----------------
class AddToCartRequest(BaseModel):
    product_id: str
    quantity: int = 1
    configuration: Optional[ConfigurationPriceRequest] = None

class CartItemResponse(BaseModel):
    id: str
    product_id: str
    product_title: str
    image_url: str
    quantity: int
    unit_price: float
    total_price: float
    configuration_summary: Dict[str, Any] = {}

class CartResponse(BaseModel):
    items: List[CartItemResponse] = []
    subtotal: float
    discount: float = 0.0
    shipping: float = 0.0
    total: float
    currency: str = "NGN"

# -----------------
# Payment Enums & DTOs
# -----------------
from enum import Enum

class PaymentStatusEnum(str, Enum):
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class PaymentProviderEnum(str, Enum):
    PAYSTACK = "PAYSTACK"
    FLUTTERWAVE = "FLUTTERWAVE"
    OPAY = "OPAY"
    BANK_TRANSFER = "BANK_TRANSFER"

class PaymentGatewayInfo(BaseModel):
    id: str
    name: str
    code: PaymentProviderEnum
    description: str
    logo_icon: str
    supported_channels: List[str]
    is_active: bool = True
    badge: Optional[str] = None

class ShippingAddressInput(BaseModel):
    full_name: str
    phone_number: str
    email: str
    street: str
    city: str
    state: str
    country: str = "Nigeria"
    additional_notes: Optional[str] = None

class CheckoutItemInput(BaseModel):
    product_id: str
    quantity: int = 1
    unit_price: float
    product_title: str
    image_url: str
    configuration_snapshot: Optional[Dict[str, Any]] = None

class OrderCheckoutRequest(BaseModel):
    items: List[CheckoutItemInput]
    shipping_address: ShippingAddressInput
    customer_email: str
    customer_name: str
    customer_phone: Optional[str] = None
    discount_amount: float = 0.0
    shipping_fee: float = 0.0
    idempotency_key: Optional[str] = None

class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    product_title: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float
    configuration_snapshot: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: str
    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    shipping_address: Dict[str, Any]
    status: str
    subtotal: float
    shipping_fee: float
    discount_amount: float
    total_amount: float
    currency: str
    payment_reference: Optional[str] = None
    payment_gateway: Optional[str] = None
    paid_at: Optional[str] = None
    created_at: Optional[str] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True

class PaymentInitializeRequest(BaseModel):
    order_number: str
    provider: PaymentProviderEnum
    callback_url: Optional[str] = None
    idempotency_key: str = Field(..., description="Unique client idempotency key to prevent double charging")
    email: Optional[str] = None
    amount: Optional[float] = None

class PaymentInitializeResponse(BaseModel):
    payment_id: str
    order_number: str
    provider: PaymentProviderEnum
    provider_reference: str
    access_code: Optional[str] = None
    checkout_url: str
    amount: float
    currency: str
    status: PaymentStatusEnum
    idempotent_replay: bool = False
    created_at: str

class PaymentVerificationResponse(BaseModel):
    payment_id: str
    order_number: str
    provider: PaymentProviderEnum
    provider_reference: str
    status: PaymentStatusEnum
    amount: float
    currency: str
    channel: Optional[str] = None
    paid_at: Optional[str] = None
    gateway_message: Optional[str] = None
    order_status: str

# -----------------
# Reviews
# -----------------
class ReviewResponse(BaseModel):
    id: str
    product_id: str
    author_name: str
    rating: int
    comment: str
    is_verified: bool = True
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewCreateRequest(BaseModel):
    product_id: Optional[str] = None
    author_name: str
    rating: int = Field(5, ge=1, le=5)
    comment: str
    is_verified: bool = True

# -----------------
# Promotions
# -----------------
class PromotionResponse(BaseModel):
    id: str
    title: str
    code: Optional[str] = None
    description: Optional[str] = None
    discount_type: str = "percentage"
    discount_value: float
    banner_url: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True

# -----------------
# Configurations
# -----------------
class ConfigurationCreateRequest(BaseModel):
    product_id: str
    color_id: Optional[str] = None
    ram_id: Optional[str] = None
    storage_id: Optional[str] = None
    cpu_id: Optional[str] = None
    gpu_id: Optional[str] = None
    display_id: Optional[str] = None
    keyboard_id: Optional[str] = None
    accessory_ids: List[str] = []
    artwork: Optional[ArtworkConfig] = None

class ConfigurationResponse(BaseModel):
    product_id: str
    product_title: str
    base_price: float
    total_price: float
    price_breakdown: List[PriceBreakdownItem] = []
    configuration_snapshot: Dict[str, Any] = {}
    specs_summary: Dict[str, Any] = {}

# -----------------
# Saved Builds
# -----------------
class SavedBuildCreateRequest(BaseModel):
    title: str
    product_id: str
    total_price: float
    configuration_snapshot: Dict[str, Any] = {}
    specs_summary: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    user_id: Optional[str] = None

class SavedBuildResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    title: str
    product_id: str
    image_url: Optional[str] = None
    total_price: float
    configuration_snapshot: Dict[str, Any] = {}
    specs_summary: Dict[str, Any] = {}
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

# -----------------
# Cart Operations
# -----------------
class CartItemCreateRequest(BaseModel):
    product_id: str
    quantity: int = 1
    unit_price: Optional[float] = None
    configuration_data: Optional[Dict[str, Any]] = None

class CartItemUpdateRequest(BaseModel):
    quantity: int = Field(1, ge=1)

# -----------------
# Artwork Upload
# -----------------
class ArtworkUploadResponse(BaseModel):
    success: bool = True
    image_url: str
    filename: str
    file_size: int
    content_type: str
    message: str = "Artwork uploaded successfully"

# -----------------
# Admin Schemas
# -----------------
class AdminProductCreate(BaseModel):
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
    model_3d_url: Optional[str] = None

class AdminProductUpdate(BaseModel):
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
    model_3d_url: Optional[str] = None

class AdminConfigurationCreate(BaseModel):
    category_code: str
    code: str
    name: str
    price_modifier: float = 0.0
    stock: int = 100
    is_active: bool = True
    display_order: int = 0
    metadata_json: Optional[Dict[str, Any]] = None

class AdminOrderUpdate(BaseModel):
    status: str # PENDING_PAYMENT, PAID, PROCESSING, CUSTOM_BUILD, READY_FOR_SHIPPING, SHIPPED, DELIVERED, CANCELLED
    payment_reference: Optional[str] = None
    payment_gateway: Optional[str] = None

class AdminCustomerResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: str = "customer"
    reward_points: int = 0
    total_orders: int = 0
    total_spent: float = 0.0
    created_at: Optional[str] = None

class AdminAnalyticsResponse(BaseModel):
    total_revenue: float
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_customers: int
    total_products: int
    top_selling_laptops: List[Dict[str, Any]] = []
    payment_method_breakdown: Dict[str, int] = {}

# -----------------
# Authentication & Accounts
# -----------------
class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: str = Field(..., max_length=150)
    password: str = Field(..., min_length=6, max_length=100)
    phone: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class AdminLoginRequest(BaseModel):
    email: str
    password: str

class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str
    reward_points: int = 0
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 604800  # 7 days
    user: UserProfileResponse

class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

# -----------------
# Website Visitor Analytics
# -----------------
class VisitorTrackRequest(BaseModel):
    session_id: Optional[str] = None
    page_path: Optional[str] = "/"
    referrer: Optional[str] = None

class VisitorTrackResponse(BaseModel):
    status: str = "recorded"
    date: str
    today_total_visits: int
    today_unique_visitors: int
    today_page_views: int

class DailyVisitorMetricItem(BaseModel):
    date: str
    total_visits: int
    unique_visitors: int
    page_views: int

    class Config:
        from_attributes = True

class VisitorAnalyticsResponse(BaseModel):
    today: DailyVisitorMetricItem
    yesterday: Optional[DailyVisitorMetricItem] = None
    total_lifetime_visits: int
    total_lifetime_uniques: int
    daily_history: List[DailyVisitorMetricItem] = []

class CompanyBankDetailsResponse(BaseModel):
    bank_name: str
    account_name: str
    account_number: str
    currency: str = "NGN"
    whatsapp_confirmation: str
    instructions: str

