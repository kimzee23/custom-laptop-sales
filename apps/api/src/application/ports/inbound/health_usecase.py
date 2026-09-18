from abc import ABC, abstractmethod
from typing import Dict, Any

class HealthUseCase(ABC):
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        pass
