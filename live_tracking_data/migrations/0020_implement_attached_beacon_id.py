# Generated by Django 5.0.6 on 2024-08-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_tracking_data', '0019_remove_implement_id_implement_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='implement',
            name='attached_beacon_id',
            field=models.CharField(default=None, max_length=100, unique=True),
        ),
    ]
