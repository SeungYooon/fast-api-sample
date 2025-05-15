from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app.core.security import ALGORITHM, SECRET_KEY
from app.models.post import Post
from app.models.user import User
from app.routers.user import get_db
from app.schemas.post import PostCreate, PostOut
from app.tasks.notify import send_notification

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
router = APIRouter(prefix="/posts", tags=["posts"])


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
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/", response_model=PostOut)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(db, token)

    db_post = Post(**post.dict(), user_id=user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    send_notification.delay(user.id)

    return db_post


@router.get("/search", response_model=list[PostOut])
def search_posts(q: str = "", db: Session = Depends(get_db)):
    return (
        db.query(Post)
        .filter((Post.title.contains(q)) | (Post.content.contains(q)))
        .all()
    )


@router.get("/", response_model=list[PostOut])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Post).offset(skip).limit(limit).all()


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(db, token)
    db_post = (
        db.query(Post)
        .filter(
            Post.id == post_id,
            Post.user_id == user.id,
        )
        .first()
    )
    if not db_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found or no permission",
        )
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(db, token)
    db_post = (
        db.query(Post)
        .filter(
            Post.id == post_id,
            Post.user_id == user.id,
        )
        .first()
    )
    if not db_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found or no permission",
        )
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}
