from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.model.review import Review

class ReviewUseCase(ABC):
    @abstractmethod
    async def create_review(self, product_id: str, author_name: str, rating: int, comment: str) -> Review:
        pass

    @abstractmethod
    async def list_reviews(self, product_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Review]:
        pass
