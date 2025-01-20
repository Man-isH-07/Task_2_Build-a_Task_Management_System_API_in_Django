from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab  # For advanced periodic schedules

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.conf.beat_schedule = {
    'send-weekly-report-every-2-minutes': {
        'task': 'task.tasks.send_weekly_report',
        'schedule': crontab(minute='*/1'),
    },
}


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

