import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from src.infrastructure.adapters.outbound.persistence.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class CategoryEntity(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    icon = Column(String(50), nullable=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)

    products = relationship("ProductEntity", back_populates="category")

class BrandEntity(Base):
    __tablename__ = "brands"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    logo_url = Column(String(500), nullable=True)

    products = relationship("ProductEntity", back_populates="brand")

class ProductEntity(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    brand_id = Column(String(36), ForeignKey("brands.id"), nullable=True)
    
    base_price = Column(Float, nullable=False, default=0.0)
    original_price = Column(Float, nullable=True)
    discount_percentage = Column(Integer, nullable=True)
    
    is_featured = Column(Boolean, default=False)
    is_flash_deal = Column(Boolean, default=False)
    is_best_seller = Column(Boolean, default=False)
    is_customizable = Column(Boolean, default=True)
    
    stock = Column(Integer, default=10)
    rating = Column(Float, default=4.8)
    review_count = Column(Integer, default=12)
    
    image_url = Column(String(500), nullable=False)
    gallery_images = Column(JSON, default=list)
    specs = Column(JSON, default=dict)
    model_3d_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    category = relationship("CategoryEntity", back_populates="products")
    brand = relationship("BrandEntity", back_populates="products")
    reviews = relationship("ReviewEntity", back_populates="product", cascade="all, delete-orphan")

class ConfigurationCategoryEntity(Base):
    __tablename__ = "configuration_categories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    display_order = Column(Integer, default=0)
    is_required = Column(Boolean, default=True)

    options = relationship("ConfigurationOptionEntity", back_populates="category", cascade="all, delete-orphan")

class ConfigurationOptionEntity(Base):
    __tablename__ = "configuration_options"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    category_id = Column(String(36), ForeignKey("configuration_categories.id"), nullable=False)
    code = Column(String(100), nullable=False)
    name = Column(String(200), nullable=False)
    price_modifier = Column(Float, default=0.0)
    stock = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    metadata_json = Column(JSON, default=dict)

    category = relationship("ConfigurationCategoryEntity", back_populates="options")

class CartEntity(Base):
    __tablename__ = "carts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(100), nullable=True)
    session_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    items = relationship("CartItemEntity", back_populates="cart", cascade="all, delete-orphan")

class CartItemEntity(Base):
    __tablename__ = "cart_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    cart_id = Column(String(36), ForeignKey("carts.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    configuration_data = Column(JSON, default=dict)
    
    cart = relationship("CartEntity", back_populates="items")
    product = relationship("ProductEntity")

class OrderEntity(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_number = Column(String(50), nullable=False, unique=True)
    user_id = Column(String(100), nullable=True)
    customer_name = Column(String(150), nullable=False)
    customer_email = Column(String(150), nullable=False)
    customer_phone = Column(String(50), nullable=True)
    shipping_address = Column(JSON, nullable=False)
    
    status = Column(String(50), default="PENDING_PAYMENT")
    subtotal = Column(Float, nullable=False)
    shipping_fee = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="NGN")
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    paid_at = Column(DateTime, nullable=True)
    payment_reference = Column(String(100), nullable=True)
    payment_gateway = Column(String(50), nullable=True)

    items = relationship("OrderItemEntity", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("PaymentEntity", back_populates="order", cascade="all, delete-orphan")

class OrderItemEntity(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    configuration_snapshot = Column(JSON, default=dict)

    order = relationship("OrderEntity", back_populates="items")
    product = relationship("ProductEntity")

class PaymentEntity(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)
    user_id = Column(String(100), nullable=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="NGN")
    status = Column(String(30), default="INITIATED", index=True, nullable=False)
    provider = Column(String(30), nullable=False)
    provider_reference = Column(String(150), unique=True, index=True, nullable=False)
    access_code = Column(String(150), nullable=True)
    checkout_url = Column(String(500), nullable=True)
    idempotency_key = Column(String(150), unique=True, index=True, nullable=False)
    channel = Column(String(50), nullable=True)
    gateway_response = Column(JSON, default=dict)
    failure_reason = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    paid_at = Column(DateTime, nullable=True)

    order = relationship("OrderEntity", back_populates="payments")

class ProcessedWebhookEntity(Base):
    __tablename__ = "processed_webhook_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    provider = Column(String(30), nullable=False)
    event_id = Column(String(150), unique=True, index=True, nullable=False)
    event_type = Column(String(100), nullable=False)
    payload_hash = Column(String(100), nullable=True)
    processed_at = Column(DateTime, default=utc_now)
    raw_payload = Column(JSON, default=dict)

class ReviewEntity(Base):
    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    author_name = Column(String(100), nullable=False)
    rating = Column(Integer, default=5)
    comment = Column(Text, nullable=False)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    product = relationship("ProductEntity", back_populates="reviews")

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(String(20), default="customer")
    reward_points = Column(Integer, default=500)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    addresses = relationship("AddressEntity", back_populates="user", cascade="all, delete-orphan")
    saved_configurations = relationship("SavedConfigurationEntity", back_populates="user", cascade="all, delete-orphan")

class AddressEntity(Base):
    __tablename__ = "addresses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(50), default="Home")
    full_name = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=False)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(50), default="Nigeria")
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("UserEntity", back_populates="addresses")

class SavedConfigurationEntity(Base):
    __tablename__ = "saved_configurations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    image_url = Column(String(500), nullable=True)
    total_price = Column(Float, nullable=False)
    configuration_snapshot = Column(JSON, default=dict)
    specs_summary = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("UserEntity", back_populates="saved_configurations")
    product = relationship("ProductEntity")

class PromotionEntity(Base):
    __tablename__ = "promotions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    code = Column(String(50), nullable=True, unique=True)
    description = Column(Text, nullable=True)
    discount_type = Column(String(20), default="percentage")
    discount_value = Column(Float, default=10.0)
    banner_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime, default=utc_now)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)

class DailyVisitorMetricEntity(Base):
    __tablename__ = "daily_visitor_metrics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    date = Column(String(10), nullable=False, unique=True, index=True)
    total_visits = Column(Integer, default=0, nullable=False)
    unique_visitors = Column(Integer, default=0, nullable=False)
    page_views = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class VisitorLogEntity(Base):
    __tablename__ = "visitor_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    date = Column(String(10), nullable=False, index=True)
    visitor_hash = Column(String(64), nullable=False, index=True)
    session_id = Column(String(100), nullable=True)
    page_path = Column(String(255), nullable=True)
    user_agent = Column(String(500), nullable=True)
    referrer = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=utc_now)
