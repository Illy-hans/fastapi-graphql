from celery import Celery
from app.config.settings import settings
from celery.schedules import crontab

app: Celery = Celery('tasks',
        broker='redis://localhost:6379/0',
        # For development the results are logged with the rest of the data
        result_backend=settings.DATABASE_URL,
        include=['app.tasks']) 


app.conf.update(
    task_serialiser='json',
    result_serialiser='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    imports=('app.tasks'),
    broker_connection_retry_on_startup =True
)

# Scheduler runs the task at 12.01 daily. 
app.conf.beat_schedule = {
    'calculate-daily-balances': {
        'task': 'app.tasks.calculate_daily_balances',
        'schedule': crontab(hour=0, minute=1), 
        # For DEVELOPMENT: Runs task every 2m
        # 'schedule': crontab(minute='*/2'),  
    },
}

# TO START WORKER:
# celery -A celery_config  worker --loglevel=info

# TO START WORKER IN DEBUG MODE:
# celery -A celery_config  worker --loglevel=DEBUG/info