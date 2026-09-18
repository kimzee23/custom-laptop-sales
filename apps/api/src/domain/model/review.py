from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Review:
    id: str
    product_id: str
    author_name: str
    rating: int = 5
    comment: str = ""
    is_verified: bool = True
    created_at: Optional[datetime] = None
