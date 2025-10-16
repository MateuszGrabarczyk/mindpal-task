from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.post import Post
from app.services import post_service

router = APIRouter(
    tags=["items"],
)


@router.post("/fetch", status_code=status.HTTP_201_CREATED)
async def fetch_and_store_items(db: AsyncSession = Depends(get_db)):
    posts_data = await post_service.fetch_posts_from_api()
    new_records_count = await post_service.save_posts_to_db(db, posts_data)
    return {
        "message": f"Successfully fetched and stored {new_records_count} new items."
    }


@router.get("/items", response_model=List[Post])
async def get_items(
    skip: int = 0,
    limit: int = Query(default=5, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    items = await post_service.get_latest_posts(db=db, skip=skip, limit=limit)
    return items
