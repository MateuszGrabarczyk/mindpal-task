import uuid
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    body: str
    source_id: int


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
