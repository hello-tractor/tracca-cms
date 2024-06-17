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
    position = models.CharField(max_length=255, default=0.0)
    engine_state = models.CharField(max_length=50, null=True, blank=True)
    asset_battery = models.FloatField(null=True, blank=True)
    raw_value = models.CharField(max_length=255, null=True, blank=True)
    sim_iccid = models.CharField(max_length=50, null=True, blank=True)
    other_data = models.JSONField()

    def __str__(self):
        return f"Device {self.device_id} - {self.latitude}, {self.longitude}"