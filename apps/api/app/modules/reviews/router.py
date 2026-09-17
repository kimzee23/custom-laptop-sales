import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models import Review, Product
from app.schemas import ReviewResponse, ReviewCreateRequest

router = APIRouter(prefix="/reviews", tags=["Reviews & Ratings"])

@router.get("", response_model=List[ReviewResponse])
async def list_reviews(
    product_id: Optional[str] = Query(None, description="Filter reviews by product ID"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Lists product customer reviews with optional filtering by product ID.
    """
    stmt = select(Review)
    if product_id:
        stmt = stmt.where(Review.product_id == product_id)
    
    stmt = stmt.order_by(Review.created_at.desc()).offset((page - 1) * limit).limit(limit)
    res = await db.execute(stmt)
    reviews = res.scalars().all()
    
    return [
        ReviewResponse(
            id=r.id,
            product_id=r.product_id,
            author_name=r.author_name,
            rating=r.rating,
            comment=r.comment,
            is_verified=r.is_verified,
            created_at=r.created_at.isoformat() if r.created_at else None
        )
        for r in reviews
    ]

@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    body: ReviewCreateRequest,
    product_id: Optional[str] = Query(None, description="Optional product ID if not in body"),
    db: AsyncSession = Depends(get_db)
):
    """
    Submits a new customer rating and review for a laptop.
    """
    effective_prod_id = body.product_id or product_id
    if not effective_prod_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="product_id must be provided in body or query param"
        )

    # Check product exists
    p_stmt = select(Product).where(Product.id == effective_prod_id)
    p_res = await db.execute(p_stmt)
    product = p_res.scalars().first()

    new_review = Review(
        id=str(uuid.uuid4()),
        product_id=effective_prod_id,
        author_name=body.author_name,
        rating=body.rating,
        comment=body.comment,
        is_verified=body.is_verified
    )
    db.add(new_review)
    await db.flush()

    if product:
        # Recalculate average rating
        avg_stmt = select(func.avg(Review.rating), func.count(Review.id)).where(Review.product_id == effective_prod_id)
        avg_res = await db.execute(avg_stmt)
        avg_rating, count = avg_res.first() or (body.rating, 1)
        product.rating = round(float(avg_rating or body.rating), 1)
        product.review_count = int(count or 1)

    await db.commit()
    await db.refresh(new_review)

    return ReviewResponse(
        id=new_review.id,
        product_id=new_review.product_id,
        author_name=new_review.author_name,
        rating=new_review.rating,
        comment=new_review.comment,
        is_verified=new_review.is_verified,
        created_at=new_review.created_at.isoformat() if new_review.created_at else None
    )
