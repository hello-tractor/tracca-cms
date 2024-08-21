from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Create a periodic task for fetching and storing live tracking data'

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=2,
            period=IntervalSchedule.SECONDS,
        )

        task, created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Fetch and store live tracking data',
            task='live_tracking_data.tasks.fetch_traccar_data',
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Periodic task created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Periodic task already exists'))
