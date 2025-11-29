from app import app
from celery import Celery, Task
from datetime import timedelta

def make_celery(app):
    # 1. Initialize Celery with the App Name
    celery = Celery(
        app.import_name,
        # 2. Use Explicit New-Style Settings (Lowercase)
        broker="redis://127.0.0.1:6379/0",
        backend="redis://127.0.0.1:6379/0"
    )

    # 3. Explicitly set configuration to avoid mixing keys
    celery.conf.update(
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",
        timezone="Asia/Kolkata",
        enable_utc=False,
    )

    # 4. Context Task (Required for Flask Database Access)
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Create the instance
celery = make_celery(app)

# 5. Define Schedule (Use 'beat_schedule' - Lowercase)
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'test-heartbeat': {
        'task': 'send_daily_reminders', # We reuse an existing task
        'schedule': timedelta(seconds=30), 
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

# 6. Import tasks at the bottom
import tasks