from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class live_tracking_data(models.Model):
    device_id = models.IntegerField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    other_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Device {self.device_id} - {self.latitude}, {self.longitude}"