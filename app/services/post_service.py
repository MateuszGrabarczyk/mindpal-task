import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.config import settings
from app.models import post as post_model


async def fetch_posts_from_api() -> list[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(settings.EXTERNAL_API_URL, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Request to external API timed out.",
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"An error occurred while requesting the external API: {exc}",
            )


async def save_posts_to_db(db: AsyncSession, posts_data: list[dict]):
    stmt = select(post_model.Post.source_id)
    result = await db.execute(stmt)
    existing_ids = set(result.scalars().all())

    new_posts = []
    for item_data in posts_data:
        if item_data["id"] not in existing_ids:
            post = post_model.Post(
                source_id=item_data["id"],
                title=item_data["title"],
                body=item_data["body"],
            )
            new_posts.append(post)

    if new_posts:
        db.add_all(new_posts)
        await db.flush()

    return len(new_posts)


async def get_latest_posts(
    db: AsyncSession, skip: int = 0, limit: int = 5
) -> list[post_model.Post]:
    stmt = (
        select(post_model.Post)
        .order_by(post_model.Post.source_id.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(stmt)
    return list(result.scalars().all())
