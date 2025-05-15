import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_BACKEND_URL"),
)

celery_app.conf.timezone = "Asia/Seoul"

# app/tasks 경로에서 task 자동 탐색
celery_app.autodiscover_tasks(["app.tasks"])
