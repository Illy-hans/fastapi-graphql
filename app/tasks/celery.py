from celery import Celery
from app.config.settings import settings
from celery.schedules import crontab

app: Celery = Celery('my_app',
        broker='redis://localhost:6379/0',
        result_backend=settings.DATABASE_URL) 

app.conf.update(
    task_serialiser='json',
    result_serialiser='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)


# Scheduler runs the task at 12.01 daily. 
app.conf.beat_schedule = {
    'calculate-daily-balances': {
        'task': 'tasks.calculate_daily_balances',
        'schedule': crontab(hour=0, minute=1), 
    },
}