from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentOut
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.routers.user import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
router = APIRouter(prefix="/comments", tags=["comments"])

def get_current_user(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/{post_id}", response_model=CommentOut)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(db, token)
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = Comment(content=comment.content, user_id=user.id, post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}", response_model=list[CommentOut])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = get_current_user(db, token)
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user.id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found or no permission")

    db_comment.content = comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = get_current_user(db, token)
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user.id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found or no permission")

    db.delete(db_comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

