from fastapi import APIRouter, Depends
from src.application.service.health_service import HealthService
from src.infrastructure.adapters.inbound.rest.dependencies import get_health_service

router = APIRouter(prefix="/health", tags=["Health & Status"])

@router.get("")
async def health_check(health_service: HealthService = Depends(get_health_service)):
    return await health_service.check_health()
