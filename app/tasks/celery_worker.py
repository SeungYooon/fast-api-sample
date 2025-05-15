from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",  # 로컬 Redis 기준
    backend="redis://localhost:6379/0",
)

celery_app.conf.timezone = "Asia/Seoul"
