from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentOut(CommentCreate):
    id: int
    post_id: int
    user_id: int

    class Config:
        orm_mode = True
