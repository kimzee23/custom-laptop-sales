from typing import Dict, Any
from src.application.ports.inbound.health_usecase import HealthUseCase

class HealthService(HealthUseCase):
    def __init__(self, db_check_fn):
        self.db_check = db_check_fn

    async def check_health(self) -> Dict[str, Any]:
        db_healthy = False
        try:
            db_healthy = await self.db_check()
        except Exception:
            db_healthy = False

        return {
            "status": "healthy" if db_healthy else "degraded",
            "database": "connected" if db_healthy else "disconnected",
            "service": "Custom Laptop Sales API (Hexagonal Architecture)",
            "version": "1.0.0"
        }
