import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from src.domain.model.analytics import DailyVisitorMetric, VisitorLog
from src.application.ports.inbound.analytics_usecase import AnalyticsUseCase
from src.application.ports.outbound.analytics_repository_port import AnalyticsRepositoryPort

class AnalyticsService(AnalyticsUseCase):
    def __init__(self, analytics_repository: AnalyticsRepositoryPort):
        self.analytics_repo = analytics_repository

    async def track_visit(
        self,
        visitor_hash: str,
        session_id: Optional[str] = None,
        page_path: Optional[str] = None,
        user_agent: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> Dict[str, Any]:
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        has_visited = await self.analytics_repo.has_visited_today(today_str, visitor_hash)
        is_unique = not has_visited

        log = VisitorLog(
            id=str(uuid.uuid4()),
            date=today_str,
            visitor_hash=visitor_hash,
            session_id=session_id,
            page_path=page_path,
            user_agent=user_agent,
            referrer=referrer,
            created_at=datetime.now(timezone.utc)
        )
        await self.analytics_repo.record_visitor_log(log)
        metric = await self.analytics_repo.increment_metrics(today_str, is_unique=is_unique)

        return {
            "date": metric.date,
            "total_visits": metric.total_visits,
            "unique_visitors": metric.unique_visitors,
            "is_unique": is_unique
        }

    async def get_daily_metrics(self, days: int = 30) -> List[DailyVisitorMetric]:
        return await self.analytics_repo.get_metrics_range(days)

    async def get_summary_stats(self) -> Dict[str, Any]:
        return await self.analytics_repo.get_totals()
