
from pydantic import BaseModel


class ReviewCreate(BaseModel):
    productCode: str
    orderId: str
    orderEntryId: str
    rating: int
    headline: str | None = None
    reviewText: str | None = None
    reviewerAlias: str