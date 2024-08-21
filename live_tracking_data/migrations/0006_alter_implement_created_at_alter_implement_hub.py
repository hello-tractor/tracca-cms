# Generated by Django 5.0.6 on 2024-08-21 07:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_tracking_data', '0005_alter_hubimplement_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='implement',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, max_length=100),
        ),
        migrations.AlterField(
            model_name='implement',
            name='hub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='live_tracking_data.hub'),
        ),
    ]
