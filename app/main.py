
from fastapi import FastAPI

from app.database import Base, engine

from app.models.rating_staging import RatingStaging

from app.routers.review_router import router as review_router

from app.routers.moderation_router import router as moderation_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Croma Review Service",
    version="1.0.0"
)

app.include_router(review_router)

app.include_router(moderation_router)

@app.get("/")
def home():
    return {
        "message": "Croma Review Service is running"
    }