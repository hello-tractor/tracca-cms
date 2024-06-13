from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class live_tracking_data(models.Model):
    device_id = models.IntegerField()
    raw_data = models.JSONField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Device {self.device_id} data at {self.timestamp}"