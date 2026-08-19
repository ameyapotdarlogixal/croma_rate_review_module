
from sqlalchemy import Column, String, Integer, Text, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class RatingStaging(Base):
    __tablename__ = "rating_staging"

    staging_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_channel = Column(String(20), nullable=False)

    product_code = Column(String(50), nullable=False)

    customer_id = Column(String(50), nullable=True)

    order_id = Column(String(50), nullable=True)

    order_entry_id = Column(String(50), nullable=True)

    rating_value = Column(Integer, nullable=False)

    headline = Column(String(255))

    review_text = Column(Text)

    reviewer_alias = Column(String(100))

    moderation_status = Column(String(20), default="RECEIVED")

    ai_validation_status = Column(String(20), nullable=True)

    ai_validation_score = Column(Float, nullable=True)

    ai_validation_flags = Column(Text, nullable=True)

    ai_triggered_by = Column(String(100), nullable=True)

    ai_triggered_at = Column(DateTime, nullable=True)

    requires_manual_review = Column(Boolean, default=False)

    moderated_by = Column(String(100), nullable=True)

    moderated_at = Column(DateTime, nullable=True)

    published_rating_id = Column(UUID(as_uuid=True), nullable=True)

    # review_classification = 