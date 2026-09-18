import hashlib
from fastapi import APIRouter, Depends, Request, Query, Header, status
from typing import Optional
from src.application.service.analytics_service import AnalyticsService
from src.infrastructure.adapters.inbound.rest.dependencies import get_analytics_service
from src.infrastructure.adapters.inbound.rest.dtos.schemas import TrackVisitRequest
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(prefix="/analytics", tags=["Traffic & Visitor Analytics"])

def _get_visitor_hash(request: Request, user_agent: Optional[str], session_id: Optional[str]) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "unknown")
    raw = f"{ip}_{user_agent or 'unknown'}_{session_id or ''}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

@router.post("/track")
async def track_visit(
    request: Request,
    req: TrackVisitRequest = TrackVisitRequest(),
    user_agent: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    sid = req.session_id or x_session_id
    ua = req.user_agent or user_agent
    visitor_hash = _get_visitor_hash(request, ua, sid)

    result = await analytics_service.track_visit(
        visitor_hash=visitor_hash,
        session_id=sid,
        page_path=req.page_path,
        user_agent=ua,
        referrer=req.referrer
    )
    return api_response(data=result, message="Visit tracked successfully.")

@router.get("/daily-visits")
async def get_daily_visits(
    days: int = Query(30, ge=1, le=90),
    analytics_service: AnalyticsService = Depends(get_analytics_service)
):
    metrics = await analytics_service.get_daily_metrics(days=days)
    return [
        {
            "id": m.id,
            "date": m.date,
            "total_visits": m.total_visits,
            "unique_visitors": m.unique_visitors,
            "page_views": m.page_views
        }
        for m in metrics
    ]

@router.get("/summary")
async def get_analytics_summary(analytics_service: AnalyticsService = Depends(get_analytics_service)):
    totals = await analytics_service.get_summary_stats()
    return api_response(data=totals, message="Traffic summary retrieved.")
