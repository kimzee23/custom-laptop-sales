from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Address:
    id: str
    user_id: str
    title: str = "Home"
    full_name: str = ""
    phone: str = ""
    street: str = ""
    city: str = ""
    state: str = ""
    country: str = "Nigeria"
    is_default: bool = False
    created_at: Optional[datetime] = None

@dataclass
class User:
    id: str
    name: str
    email: str
    hashed_password: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = "customer"
    reward_points: int = 500
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    addresses: List[Address] = field(default_factory=list)
