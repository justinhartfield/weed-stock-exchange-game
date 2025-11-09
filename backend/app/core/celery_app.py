from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "strain_exchange",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.data_sync", "app.tasks.market_events", "app.tasks.bet_settlement"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "sync-strain-data-every-5-minutes": {
            "task": "app.tasks.data_sync.sync_strain_data_task",
            "schedule": 300.0,  # 5 minutes
        },
        "settle-expired-bets-hourly": {
            "task": "app.tasks.bet_settlement.settle_expired_bets_task",
            "schedule": 3600.0,  # 1 hour
        },
    },
)
