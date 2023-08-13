"""
CELERY WORKER MANAGE COMMAND:
celery -A core worker -l INFO

START CELERY BEAT SERVICE:
celery -A core beat

EMBED BEAT INSIDE THE WORKER - IF YOU HAVE ONLY ONE WORKER!:
celery -A core worker -B
celery -A core worker -B -l INFO
"""

import os

from celery import Celery
from celery.schedules import crontab, crontab_parser

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "grab-quotes-every-even-hour": {
        "task": "sel.tasks.grab_quotes",
        # "schedule": crontab(minute="1-59/2"),  # every even minute
        "schedule": crontab(minute="0", hour="1-23/2"),  # every even hour
        "args": (url := r'https://quotes.toscrape.com/', quote_qty := 5,)
    }
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')