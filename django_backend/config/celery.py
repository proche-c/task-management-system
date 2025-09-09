from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# instance of celery
app = Celery('config')

# CLoad Django config (celery namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')

#config celery broker, which is the sistem that manage task qeues(redis)
app.conf.broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')

# config where celery will save the tasks
app.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

# define logs format
app.conf.worker_log_format = '[%(levelname)s/%(processName)s] %(message)s'

# define specific tasks logs format
app.conf.worker_task_log_format = '[%(levelname)s/%(processName)s] %(task_name)s: %(message)s'

# auto discover tasks at apps at INSTALLED_APPS
app.autodiscover_tasks()

# celery beat conf
app.conf.beat_schedule = {
    'daily_task_summary': {
        'task': 'apps.tasks.tasks.generate_daily_summary',
        'schedule': crontab(hour=6, minute=0),
    },
    'hourly_overdue_check': {
        'task': 'apps.tasks.tasks.check_overdue_tasks',
        'schedule': crontab(minute=0),
    },
}