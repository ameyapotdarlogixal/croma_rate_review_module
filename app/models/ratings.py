
import uuid

from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Ratings(Base):
    __tablename__ = "ratings"

    rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_staging_id = Column(UUID(as_uuid=True), nullable=False)

    product_code = Column(String(50), nullable=False)

    customer_id = Column(String(50))

    order_id = Column(String(50))

    order_entry_id = Column(String(50))

    rating_value = Column(Integer, nullable=False)

    verified_purchase = Column(Boolean, default=True)

    source_channel = Column(String(20))

    review_classification = Column(String(10), nullable=True)

    status = Column(String(20), default="APPROVED")

    ai_moderation_score = Column(Float, nullable=True)

    ai_validation_flags = Column(String, nullable=True)

    ai_assisted = Column(Boolean, default=False)

    approved_by = Column(String(100), nullable=False)

    approved_at = Column(DateTime, nullable=False)

    blocked_by = Column(String(100), nullable=True)

    blocked_at = Column(DateTime, nullable=True)

    block_reason = Column(String, nullable=True)