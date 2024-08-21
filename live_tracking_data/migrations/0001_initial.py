# Generated by Django 5.0.6 on 2024-08-15 16:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace_id', models.CharField(max_length=100, unique=True)),
                ('instance_id', models.CharField(max_length=100)),
                ('beacon_rssi', models.CharField(blank=True, max_length=100, null=True)),
                ('attached_to', models.CharField(blank=True, max_length=100, null=True)),
                ('attached_time', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('device_imei', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(max_length=50)),
                ('disabled', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField()),
                ('position_id', models.IntegerField(blank=True, null=True)),
                ('group_id', models.IntegerField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('contact', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('attributes', models.JSONField(default=dict)),
                ('active_beacon', models.CharField(blank=True, max_length=100, null=True)),
                ('active_implement', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImplementBrand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='live_tracking_data',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('device_id', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('speed', models.FloatField(default=0.0)),
                ('fuel_frequency', models.FloatField(blank=True, max_length=100, null=True)),
                ('position', models.CharField(default=0.0, max_length=255)),
                ('engine_state', models.CharField(blank=True, max_length=50, null=True)),
                ('asset_battery', models.FloatField(blank=True, null=True)),
                ('raw_value', models.CharField(blank=True, max_length=255, null=True)),
                ('sim_iccid', models.CharField(blank=True, max_length=100, null=True)),
                ('other_data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='NewDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100, unique=True)),
                ('unique_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Implement',
            fields=[
                ('serial_number', models.CharField(default=None, max_length=100, primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, max_length=100)),
                ('location', models.CharField(choices=[('KE', 'Kenya'), ('RW', 'Rwanda'), ('UG', 'Uganda'), ('NG', 'Nigeria'), ('ET', 'Ethiopia'), ('TZ', 'Tanzania')], default='KE', max_length=100)),
                ('attached_beacon_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='implement', to='live_tracking_data.beacon')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='live_tracking_data.implementbrand')),
            ],
        ),
        migrations.CreateModel(
            name='ImplementHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('days_used', models.IntegerField(blank=True, null=True)),
                ('current_device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_implements', to='live_tracking_data.device')),
                ('implement_serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='live_tracking_data.implement')),
                ('initial_device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='initial_implements', to='live_tracking_data.device')),
            ],
            options={
                'unique_together': {('implement_serial', 'start_date')},
            },
        ),
    ]
