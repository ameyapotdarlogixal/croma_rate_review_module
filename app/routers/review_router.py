
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.review_schema import ReviewCreate
from app.models.rating_staging import RatingStaging
from app.core.dependencies import get_db

router = APIRouter(prefix="/api/v1/reviews", tags=["Reviews"])


@router.post("")
def submit_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = RatingStaging(
        source_channel="DIRECT_WEBSITE",
        product_code=review.productCode,
        customer_id="demo_customer",
        order_id=review.orderId,
        order_entry_id=review.orderEntryId,
        rating_value=review.rating,
        headline=review.headline,
        review_text=review.reviewText,
        reviewer_alias=review.reviewerAlias,
        moderation_status="RECEIVED"
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "stagingId": str(new_review.staging_id),
        "moderationStatus": new_review.moderation_status,
        "message": "Thank you. Your review has been received and is awaiting moderation."
    }