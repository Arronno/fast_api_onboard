from pydantic import BaseModel


class PostCreate(BaseModel):
    name: str
    content: str


class PostResponse(BaseModel):
    name: str
    content: str
