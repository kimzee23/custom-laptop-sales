from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.domain.model.analytics import DailyVisitorMetric

class AnalyticsUseCase(ABC):
    @abstractmethod
    async def track_visit(
        self,
        visitor_hash: str,
        session_id: Optional[str] = None,
        page_path: Optional[str] = None,
        user_agent: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_daily_metrics(self, days: int = 30) -> List[DailyVisitorMetric]:
        pass

    @abstractmethod
    async def get_summary_stats(self) -> Dict[str, Any]:
        pass
