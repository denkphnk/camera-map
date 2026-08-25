from celery import Celery
from src.core.config import settings

celery_app = Celery(
    "camera_map",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    # include=["src.tasks.video_tasks"],  # Пока нет задач — просто закомментируй
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    result_expires=3600,
)