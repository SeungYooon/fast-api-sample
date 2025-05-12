from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.comment import Comment
from app.routers.user import get_db, get_current_user
from app.core.security import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

router = APIRouter(prefix="/admin", tags=["admin"])

def get_current_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(db, token)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/posts")
def get_all_posts(db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return db.query(Post).all()

@router.delete("/posts/{post_id}")
def delete_any_post(post_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted by admin"}

@router.get("/comments")
def get_all_comments(db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return db.query(Comment).all()

@router.delete("/comments/{comment_id}")
def delete_any_comment(comment_id: int, db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted by admin"}
