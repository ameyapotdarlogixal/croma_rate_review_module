
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from datetime import datetime

from app.schemas.moderation_schema import AIAssistRequest

from app.core.dependencies import get_db
from app.models.rating_staging import RatingStaging


from app.models.ratings import Ratings
from app.schemas.moderation_schema import ApproveRequest

router = APIRouter(
    prefix="/api/v1/moderation",
    tags=["Moderation"]
)


@router.get("/queue")
def get_moderation_queue(db: Session = Depends(get_db)):
    reviews = db.query(RatingStaging).filter(
        RatingStaging.moderation_status == "RECEIVED"
    ).all()

    return reviews



@router.post("/ai-assist")
def ai_assist(request: AIAssistRequest, db: Session = Depends(get_db)):
    results = []

    for staging_id in request.stagingIds:
        review = db.query(RatingStaging).filter(
            RatingStaging.staging_id == staging_id
        ).first()

        if review:
            review.ai_validation_status = "PASSED"
            review.ai_validation_score = 91.5
            review.ai_validation_flags = "{}"
            review.ai_triggered_by = request.triggeredBy
            review.ai_triggered_at = datetime.utcnow()
            review.moderation_status = "AI_SCORED"

            if review.rating_value <= 2 or review.ai_validation_status == "FLAGGED":
                review.requires_manual_review = True
            else:
                review.requires_manual_review = False

            db.commit()
            db.refresh(review)

            results.append({
                "stagingId": str(review.staging_id),
                "aiValidationScore": review.ai_validation_score,
                "aiValidationStatus": review.ai_validation_status,
                "moderationStatus": review.moderation_status
            })

    return {"results": results}



@router.post("/{staging_id}/approve")
def approve_review(
    staging_id: str,
    request: ApproveRequest,
    db: Session = Depends(get_db)
):
    review = db.query(RatingStaging).filter(
        RatingStaging.staging_id == staging_id
    ).first()

    if not review:
        return {"error": "Review not found"}

    if review.moderation_status != "AI_SCORED":
        return {
            "error": "Run AI Assist before approval."
        }

    new_rating = Ratings(
        source_staging_id=review.staging_id,
        product_code=review.product_code,
        customer_id=review.customer_id,
        order_id=review.order_id,
        order_entry_id=review.order_entry_id,
        rating_value=review.rating_value,
        verified_purchase=True,
        source_channel=review.source_channel,
        review_classification=review.review_classification,
        status="APPROVED",
        ai_moderation_score=review.ai_validation_score,
        ai_validation_flags=review.ai_validation_flags,
        ai_assisted=review.ai_validation_score is not None,
        approved_by=request.approvedBy,
        approved_at=datetime.utcnow()
    )

    db.add(new_rating)
    db.flush()

    review.moderation_status = "PUBLISHED"
    review.moderated_by = request.approvedBy
    review.moderated_at = datetime.utcnow()
    review.published_rating_id = new_rating.rating_id

    db.commit()

    return {
        "ratingId": str(new_rating.rating_id),
        "stagingId": str(review.staging_id),
        "moderationStatus": "PUBLISHED",
        "message": "Review published successfully."
    }