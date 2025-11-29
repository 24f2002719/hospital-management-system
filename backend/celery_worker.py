from app import app
from celery import Celery, Task
from datetime import timedelta

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://127.0.0.1:6379/0",
        backend="redis://127.0.0.1:6379/0"
    )

    celery.conf.update(
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",
        timezone="Asia/Kolkata",
        enable_utc=False,
    )

    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

from celery.schedules import crontab

celery.conf.beat_schedule = {
    'test-heartbeat': {
        'task': 'send_daily_reminders', 
        'schedule': timedelta(seconds=600), 
    },
    'daily-reminder-every-morning': {
        'task': 'send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    'monthly-report-first-day': {
        'task': 'send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}


import tasks