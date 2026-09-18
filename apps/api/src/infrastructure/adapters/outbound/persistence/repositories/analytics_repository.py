from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from src.domain.model.analytics import DailyVisitorMetric, VisitorLog
from src.application.ports.outbound.analytics_repository_port import AnalyticsRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import (
    DailyVisitorMetricEntity, VisitorLogEntity
)

class AnalyticsRepository(AnalyticsRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def record_visitor_log(self, log: VisitorLog) -> VisitorLog:
        entity = VisitorLogEntity(
            id=log.id,
            date=log.date,
            visitor_hash=log.visitor_hash,
            session_id=log.session_id,
            page_path=log.page_path,
            user_agent=log.user_agent,
            referrer=log.referrer,
            created_at=log.created_at
        )
        self.session.add(entity)
        await self.session.commit()
        return log

    async def has_visited_today(self, date_str: str, visitor_hash: str) -> bool:
        stmt = select(VisitorLogEntity).where(
            VisitorLogEntity.date == date_str,
            VisitorLogEntity.visitor_hash == visitor_hash
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def increment_metrics(self, date_str: str, is_unique: bool) -> DailyVisitorMetric:
        stmt = select(DailyVisitorMetricEntity).where(DailyVisitorMetricEntity.date == date_str)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()

        if not entity:
            entity = DailyVisitorMetricEntity(
                id=str(uuid.uuid4()),
                date=date_str,
                total_visits=1,
                unique_visitors=1 if is_unique else 0,
                page_views=1,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.session.add(entity)
        else:
            entity.total_visits += 1
            entity.page_views += 1
            if is_unique:
                entity.unique_visitors += 1
            entity.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(entity)
        return DailyVisitorMetric(
            id=entity.id,
            date=entity.date,
            total_visits=entity.total_visits,
            unique_visitors=entity.unique_visitors,
            page_views=entity.page_views,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    async def get_metrics_range(self, days: int = 30) -> List[DailyVisitorMetric]:
        stmt = select(DailyVisitorMetricEntity).order_by(desc(DailyVisitorMetricEntity.date)).limit(days)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            DailyVisitorMetric(
                id=e.id,
                date=e.date,
                total_visits=e.total_visits,
                unique_visitors=e.unique_visitors,
                page_views=e.page_views,
                created_at=e.created_at,
                updated_at=e.updated_at
            )
            for e in entities
        ]

    async def get_totals(self) -> Dict[str, Any]:
        stmt = select(
            func.sum(DailyVisitorMetricEntity.total_visits),
            func.sum(DailyVisitorMetricEntity.unique_visitors),
            func.sum(DailyVisitorMetricEntity.page_views)
        )
        res = await self.session.execute(stmt)
        total_visits, unique_visitors, page_views = res.one_or_none() or (0, 0, 0)
        return {
            "total_visits": total_visits or 0,
            "unique_visitors": unique_visitors or 0,
            "page_views": page_views or 0
        }
