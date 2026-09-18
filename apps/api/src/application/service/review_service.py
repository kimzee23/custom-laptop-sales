import uuid
from datetime import datetime, timezone
from typing import List, Optional
from src.domain.model.review import Review
from src.application.ports.inbound.review_usecase import ReviewUseCase
from src.application.ports.outbound.review_repository_port import ReviewRepositoryPort

class ReviewService(ReviewUseCase):
    def __init__(self, review_repository: ReviewRepositoryPort):
        self.review_repo = review_repository

    async def create_review(self, product_id: str, author_name: str, rating: int, comment: str) -> Review:
        review = Review(
            id=str(uuid.uuid4()),
            product_id=product_id,
            author_name=author_name,
            rating=rating,
            comment=comment,
            is_verified=True,
            created_at=datetime.now(timezone.utc)
        )
        return await self.review_repo.create_review(review)

    async def list_reviews(self, product_id: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Review]:
        skip = (page - 1) * page_size
        return await self.review_repo.list_by_product(product_id=product_id, skip=skip, limit=page_size)
