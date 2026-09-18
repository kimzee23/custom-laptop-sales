from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.model.analytics import DailyVisitorMetric, VisitorLog

class AnalyticsRepositoryPort(ABC):
    @abstractmethod
    async def record_visitor_log(self, log: VisitorLog) -> VisitorLog:
        pass

    @abstractmethod
    async def has_visited_today(self, date_str: str, visitor_hash: str) -> bool:
        pass

    @abstractmethod
    async def increment_metrics(self, date_str: str, is_unique: bool) -> DailyVisitorMetric:
        pass

    @abstractmethod
    async def get_metrics_range(self, days: int = 30) -> List[DailyVisitorMetric]:
        pass

    @abstractmethod
    async def get_totals(self) -> Dict[str, Any]:
        pass
