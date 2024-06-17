from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from django.conf import settings
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-portofolio.settings')
app = Celery('asset_tracking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'fetch-live-tracking-data': {
        'task': 'live_tracking_data.tasks.fetch_tracca_data',
        'schedule': timedelta(seconds=2),  # Example: run every 2 seconds
    },
}

app.conf.timezone = 'UTC'  # Set the timezone to UTC or your desired timezone
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'