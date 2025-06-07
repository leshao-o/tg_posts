from datetime import datetime

from pydantic import BaseModel


class PostPatch(BaseModel):
    title: str | None = None
    text: str | None = None


class PostResponse(BaseModel):
    title: str
    text: str
    created_at: datetime
    

class PostAdd(BaseModel):
    title: str
    text: str


class Post(PostAdd):
    created_at: datetime
    id: int
