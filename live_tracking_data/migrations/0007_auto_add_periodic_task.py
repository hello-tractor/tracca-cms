# live_tracking_data/migrations/0007_auto_add_periodic_task.py
from django.db import migrations

def create_periodic_task(apps, schema_editor):
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
    IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')

    # Create the schedule - execute every 2 seconds
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=2,
        period='seconds',  # Corrected the period attribute
    )

    # Create the periodic task
    PeriodicTask.objects.create(
        interval=schedule,
        name='Fetch Traccar Data',
        task='live_tracking_data.tasks.fetch_tracca_data',
    )

class Migration(migrations.Migration):

    dependencies = [
        ('live_tracking_data', '0006_alter_live_tracking_data_id'),
        ('django_celery_beat', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_periodic_task),
    ]
