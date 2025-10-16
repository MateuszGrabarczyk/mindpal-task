import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.services import post_service


async def test_fetch_posts_from_api_success(mocker):
    mock_data = [{"id": 1, "title": "Test Title", "body": "Test Body"}]

    mock_response = MagicMock()
    mock_response.json.return_value = mock_data
    mock_response.raise_for_status = lambda: None

    mocker.patch(
        "httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response
    )

    posts = await post_service.fetch_posts_from_api()
    assert posts == mock_data


async def test_fetch_posts_from_api_timeout(mocker):
    mocker.patch(
        "httpx.AsyncClient.get", side_effect=httpx.TimeoutException("Request timed out")
    )

    with pytest.raises(HTTPException) as exc_info:
        await post_service.fetch_posts_from_api()
    assert exc_info.value.status_code == 504


async def test_save_posts_to_db(session: AsyncSession):
    posts_data = [
        {"id": 101, "title": "First Post", "body": "Body of first"},
        {"id": 102, "title": "Second Post", "body": "Body of second"},
    ]

    count = await post_service.save_posts_to_db(session, posts_data)
    assert count == 2

    count_again = await post_service.save_posts_to_db(session, posts_data)
    assert count_again == 0

    db_posts_result = await session.execute(select(Post))
    assert len(db_posts_result.scalars().all()) == 2


async def test_get_latest_posts(session: AsyncSession):
    for i in range(1, 11):
        post = Post(source_id=i, title=f"Title {i}", body=f"Body {i}")
        session.add(post)

    latest_posts = await post_service.get_latest_posts(session)
    assert len(latest_posts) == 5
    assert latest_posts[0].source_id == 10

    paginated_posts = await post_service.get_latest_posts(session, skip=5, limit=5)
    assert len(paginated_posts) == 5
    assert paginated_posts[0].source_id == 5
