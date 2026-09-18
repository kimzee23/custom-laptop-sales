from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from src.application.service.review_service import ReviewService
from src.infrastructure.adapters.inbound.rest.dependencies import get_review_service
from src.infrastructure.adapters.inbound.rest.dtos.schemas import ReviewCreateRequest
from src.infrastructure.adapters.inbound.rest.response import api_response

router = APIRouter(prefix="/reviews", tags=["Product Reviews"])

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_review(
    req: ReviewCreateRequest,
    review_service: ReviewService = Depends(get_review_service)
):
    rev = await review_service.create_review(
        product_id=req.product_id,
        author_name=req.author_name,
        rating=req.rating,
        comment=req.comment
    )
    return {
        "id": rev.id,
        "product_id": rev.product_id,
        "author_name": rev.author_name,
        "rating": rev.rating,
        "comment": rev.comment,
        "is_verified": rev.is_verified,
        "created_at": rev.created_at.isoformat() if rev.created_at else None
    }

@router.get("")
async def list_reviews(
    product_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    review_service: ReviewService = Depends(get_review_service)
):
    reviews = await review_service.list_reviews(product_id=product_id, page=page, page_size=page_size)
    return [
        {
            "id": r.id,
            "product_id": r.product_id,
            "author_name": r.author_name,
            "rating": r.rating,
            "comment": r.comment,
            "is_verified": r.is_verified,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in reviews
    ]
