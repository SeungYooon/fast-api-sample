
from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(PostCreate):
    id: int
    user_id: int
    class Config:
        orm_mode = True
