from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.model.review import Review

class ReviewRepositoryPort(ABC):
    @abstractmethod
    async def create_review(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def list_by_product(self, product_id: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Review]:
        pass
