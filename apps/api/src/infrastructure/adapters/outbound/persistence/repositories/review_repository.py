from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.domain.model.review import Review
from src.application.ports.outbound.review_repository_port import ReviewRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import ReviewEntity

class ReviewRepository(ReviewRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_review(self, review: Review) -> Review:
        entity = ReviewEntity(
            id=review.id,
            product_id=review.product_id,
            author_name=review.author_name,
            rating=review.rating,
            comment=review.comment,
            is_verified=review.is_verified,
            created_at=review.created_at
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return review

    async def list_by_product(self, product_id: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Review]:
        stmt = select(ReviewEntity)
        if product_id:
            stmt = stmt.where(ReviewEntity.product_id == product_id)
        stmt = stmt.order_by(desc(ReviewEntity.created_at)).offset(skip).limit(limit)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            Review(
                id=e.id,
                product_id=e.product_id,
                author_name=e.author_name,
                rating=e.rating,
                comment=e.comment,
                is_verified=e.is_verified,
                created_at=e.created_at
            )
            for e in entities
        ]
