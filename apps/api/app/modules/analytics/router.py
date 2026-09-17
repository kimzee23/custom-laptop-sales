import hashlib
from datetime import datetime, date, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models import DailyVisitorMetric, VisitorLog
from app.schemas import (
    VisitorTrackRequest,
    VisitorTrackResponse,
    VisitorAnalyticsResponse,
    DailyVisitorMetricItem
)

router = APIRouter(prefix="/analytics", tags=["Analytics & Traffic"])

def get_client_ip(request: Request) -> str:
    # Handle proxies like Render, Vercel, Cloudflare
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

def hash_visitor(ip: str, user_agent: str, session_id: Optional[str] = None) -> str:
    seed = f"{session_id or ''}:{ip}:{user_agent[:100]}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()

@router.post("/visit", response_model=VisitorTrackResponse)
async def track_page_visit(
    request: Request,
    body: Optional[VisitorTrackRequest] = None,
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    db: AsyncSession = Depends(get_db)
):
    """
    Records a page view / visitor session for the website.
    Tracks both total visits and deduplicated unique visitors per day.
    """
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    client_ip = get_client_ip(request)
    ua = user_agent or "unknown"
    session_id = body.session_id if body else None
    page_path = (body.page_path if body and body.page_path else "/")[:250]
    referrer = (body.referrer if body and body.referrer else request.headers.get("referer", ""))[:490]
    
    visitor_hash = hash_visitor(client_ip, ua, session_id)

    # 1. Check if this visitor has already been logged today
    log_stmt = select(VisitorLog).where(
        VisitorLog.date == today_str,
        VisitorLog.visitor_hash == visitor_hash
    ).limit(1)
    res = await db.execute(log_stmt)
    existing_log = res.scalar_one_or_none()

    is_unique_today = existing_log is None

    # 2. Fetch or create DailyVisitorMetric for today
    metric_stmt = select(DailyVisitorMetric).where(DailyVisitorMetric.date == today_str)
    res_metric = await db.execute(metric_stmt)
    metric = res_metric.scalar_one_or_none()

    if not metric:
        metric = DailyVisitorMetric(
            date=today_str,
            total_visits=1,
            unique_visitors=1 if is_unique_today else 0,
            page_views=1
        )
        db.add(metric)
    else:
        metric.total_visits += 1
        metric.page_views += 1
        if is_unique_today:
            metric.unique_visitors += 1

    # 3. Record raw visitor log entry
    new_log = VisitorLog(
        date=today_str,
        visitor_hash=visitor_hash,
        session_id=session_id,
        page_path=page_path,
        user_agent=ua[:490],
        referrer=referrer,
        created_at=datetime.utcnow()
    )
    db.add(new_log)

    await db.commit()
    await db.refresh(metric)

    return VisitorTrackResponse(
        status="recorded",
        date=metric.date,
        today_total_visits=metric.total_visits,
        today_unique_visitors=metric.unique_visitors,
        today_page_views=metric.page_views
    )

@router.get("/daily-visits", response_model=VisitorAnalyticsResponse)
async def get_daily_visitor_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Returns today's visits, yesterday's visits, total lifetime visits,
    and a 30-day daily breakdown of website traffic.
    """
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    yesterday_str = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Fetch last 30 days metrics
    stmt = (
        select(DailyVisitorMetric)
        .order_by(DailyVisitorMetric.date.desc())
        .limit(30)
    )
    res = await db.execute(stmt)
    metrics = res.scalars().all()

    today_metric = next((m for m in metrics if m.date == today_str), None)
    yesterday_metric = next((m for m in metrics if m.date == yesterday_str), None)

    if not today_metric:
        today_item = DailyVisitorMetricItem(
            date=today_str,
            total_visits=0,
            unique_visitors=0,
            page_views=0
        )
    else:
        today_item = DailyVisitorMetricItem.model_validate(today_metric)

    yesterday_item = (
        DailyVisitorMetricItem.model_validate(yesterday_metric)
        if yesterday_metric
        else None
    )

    # Compute totals
    totals_stmt = select(
        func.sum(DailyVisitorMetric.total_visits),
        func.sum(DailyVisitorMetric.unique_visitors)
    )
    res_totals = await db.execute(totals_stmt)
    row = res_totals.one()
    total_visits = int(row[0] or (today_item.total_visits))
    total_uniques = int(row[1] or (today_item.unique_visitors))

    return VisitorAnalyticsResponse(
        today=today_item,
        yesterday=yesterday_item,
        total_lifetime_visits=total_visits,
        total_lifetime_uniques=total_uniques,
        daily_history=[DailyVisitorMetricItem.model_validate(m) for m in metrics]
    )

@router.get("/summary")
async def get_visitor_summary(db: AsyncSession = Depends(get_db)):
    """
    Quick endpoint for widget badges or live user count on frontend.
    """
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    stmt = select(DailyVisitorMetric).where(DailyVisitorMetric.date == today_str)
    res = await db.execute(stmt)
    metric = res.scalar_one_or_none()

    return {
        "date": today_str,
        "visits_today": metric.total_visits if metric else 0,
        "unique_visitors_today": metric.unique_visitors if metric else 0,
        "page_views_today": metric.page_views if metric else 0,
    }
