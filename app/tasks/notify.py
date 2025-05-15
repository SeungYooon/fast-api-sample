from celery import shared_task
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.notification import Notification


@shared_task
def send_notification(user_id: int):
    db: Session = SessionLocal()
    try:
        message = f"유저 {user_id}가 게시글을 작성했습니다."
        db.add(Notification(user_id=user_id, message=message))
        db.commit()
        print(f"✅ 알림 저장 완료: {message}")
    finally:
        db.close()
