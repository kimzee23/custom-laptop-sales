from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class ConfigurationOption:
    id: str
    category_id: str
    code: str
    name: str
    price_modifier: float = 0.0
    stock: int = 100
    is_active: bool = True
    display_order: int = 0
    metadata_json: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConfigurationCategory:
    id: str
    code: str
    name: str
    display_order: int = 0
    is_required: bool = True
    options: List[ConfigurationOption] = field(default_factory=list)

@dataclass
class SavedConfiguration:
    id: str
    user_id: str
    title: str
    product_id: str
    image_url: Optional[str] = None
    total_price: float = 0.0
    configuration_snapshot: Dict[str, Any] = field(default_factory=dict)
    specs_summary: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None
