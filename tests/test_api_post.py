import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post


async def test_fetch_and_store_items(client: AsyncClient, mocker):
    """
    Tests the POST /fetch endpoint by mocking the service functions.
    """
    mocker.patch(
        "app.services.post_service.fetch_posts_from_api",
        return_value=[{"id": 1, "title": "API Test", "body": "API Body"}],
    )
    mocker.patch("app.services.post_service.save_posts_to_db", return_value=1)

    response = await client.post("/fetch")

    assert response.status_code == 201
    assert response.json() == {
        "message": "Successfully fetched and stored 1 new items."
    }


async def test_get_items(client: AsyncClient, session: AsyncSession):
    for i in range(1, 8):
        post = Post(source_id=i, title=f"Title {i}", body=f"Body {i}")
        session.add(post)

    response = await client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["source_id"] == 7

    response = await client.get("/items?skip=5&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["source_id"] == 2
