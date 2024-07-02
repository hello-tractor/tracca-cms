from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class live_tracking_data(models.Model):
    id = models.IntegerField(primary_key=True)
    device_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    fuel_frequency = models.FloatField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=255, default=0.0)
    engine_state = models.CharField(max_length=50, null=True, blank=True)
    asset_battery = models.FloatField(null=True, blank=True)
    raw_value = models.CharField(max_length=255, null=True, blank=True)
    sim_iccid = models.CharField(max_length=100, null=True, blank=True)
    other_data = models.JSONField()

    def __str__(self):
        return f"Device {self.device_id} - {self.latitude}, {self.longitude}"
    
class Device(models.Model):
    id = models.IntegerField(primary_key=True)  # Assuming 'id' is the primary key
    name = models.CharField(max_length=100)
    device_imei = models.CharField(max_length=50, unique=True)  # Unique ID as per your requirements
    status = models.CharField(max_length=50)
    disabled = models.BooleanField(default=False)
    last_update = models.DateTimeField()
    position_id = models.IntegerField(null=True, blank=True)
    group_id = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True, default=None)
    category = models.CharField(max_length=50, null=True, blank=True)
    attributes = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
class NewDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    unique_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    # Add other fields as needed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name