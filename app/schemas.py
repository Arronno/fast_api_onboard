import uuid

from pydantic import BaseModel
from fastapi_users import schemas


class PostCreate(BaseModel):
    name: str
    content: str


class PostResponse(BaseModel):
    name: str
    content: str


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
