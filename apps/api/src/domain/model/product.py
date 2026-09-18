from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class Category:
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0
    created_at: Optional[datetime] = None

@dataclass
class Brand:
    id: str
    name: str
    slug: str
    logo_url: Optional[str] = None

@dataclass
class Promotion:
    id: str
    title: str
    code: Optional[str] = None
    description: Optional[str] = None
    discount_type: str = "percentage"
    discount_value: float = 10.0
    banner_url: Optional[str] = None
    is_active: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: Optional[datetime] = None

@dataclass
class Product:
    id: str
    title: str
    slug: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    base_price: float = 0.0
    original_price: Optional[float] = None
    discount_percentage: Optional[int] = None
    is_featured: bool = False
    is_flash_deal: bool = False
    is_best_seller: bool = False
    is_customizable: bool = True
    stock: int = 10
    rating: float = 4.8
    review_count: int = 12
    image_url: str = ""
    gallery_images: List[str] = field(default_factory=list)
    specs: Dict[str, Any] = field(default_factory=dict)
    model_3d_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category: Optional[Category] = None
    brand: Optional[Brand] = None
