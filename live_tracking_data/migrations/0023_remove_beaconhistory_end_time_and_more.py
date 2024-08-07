# Generated by Django 5.0.6 on 2024-08-06 13:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_tracking_data', '0022_remove_beaconhistory_attached_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beaconhistory',
            name='end_time',
        ),
        migrations.AlterField(
            model_name='beaconhistory',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
