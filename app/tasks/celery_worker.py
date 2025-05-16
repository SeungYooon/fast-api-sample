# app/tasks/celery_worker.py
import os

from celery import Celery

celery_app = Celery(
    "worker",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_BACKEND_URL"],
)

celery_app.conf.timezone = "Asia/Seoul"
celery_app.autodiscover_tasks(["app.tasks"])
