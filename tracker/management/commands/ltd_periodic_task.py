from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from live_tracking_data.tasks import fetch_and_store_live_tracking_data

class Command(BaseCommand):
    help = 'Initialize periodic task for fetching and storing live tracking data'

    def handle(self, *args, **kwargs):
        # Create an interval schedule (every 0.5 minutes)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=0.5,
            period=IntervalSchedule.MINUTES,
        )

        # Create a periodic task
        PeriodicTask.objects.create(
            interval=schedule,
            name='Fetch and store live tracking data',
            task='myapp.tasks.fetch_and_store_live_tracking_data',
        )

        self.stdout.write(self.style.SUCCESS('Successfully initialized periodic task'))
