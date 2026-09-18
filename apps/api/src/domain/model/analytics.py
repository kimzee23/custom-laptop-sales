from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class DailyVisitorMetric:
    id: str
    date: str # YYYY-MM-DD
    total_visits: int = 0
    unique_visitors: int = 0
    page_views: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class VisitorLog:
    id: str
    date: str
    visitor_hash: str
    session_id: Optional[str] = None
    page_path: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    created_at: Optional[datetime] = None
