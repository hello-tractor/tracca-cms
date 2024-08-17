from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class live_tracking_data(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    device_id = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    fuel_frequency = models.FloatField(null=True, blank=True)  # Removed max_length
    position = models.CharField(max_length=255, default=0.0)
    engine_state = models.CharField(max_length=50, null=True, blank=True)
    asset_battery = models.FloatField(null=True, blank=True)
    raw_value = models.CharField(max_length=255, null=True, blank=True)
    sim_iccid = models.CharField(max_length=100, null=True, blank=True)
    other_data = models.JSONField()

    def __str__(self):
        return f"Device {self.device_id} - {self.latitude}, {self.longitude}"

class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    device_imei = models.CharField(max_length=50, unique=True)
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
    active_beacon = models.CharField(max_length=100, null=True, blank=True)
    active_implement = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.device_imei

class ImplementBrand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if ImplementBrand.objects.filter(name__iexact=self.name).exists():
            raise ValidationError(f"A brand with the name '{self.name}' already exists.")

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class NewDevice(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    unique_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Beacon(models.Model):
    namespace_id = models.CharField(max_length=100, unique=True)
    instance_id = models.CharField(max_length=100)
    beacon_rssi = models.CharField(max_length=100, null=True, blank=True)
    attached_to = models.CharField(max_length=100, null=True, blank=True)
    attached_time = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.namespace_id

class Implement(models.Model):
    serial_number = models.CharField(max_length=100, primary_key=True, blank=False, default=None)
    brand = models.ForeignKey(ImplementBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    attached_beacon_id = models.OneToOneField(Beacon, on_delete=models.CASCADE, related_name='implement')
    created_at = models.DateTimeField(max_length=100, default=timezone.now)
    location = models.CharField(max_length=100,
                                choices=[(code, name) for code, name in (
                                    ('KE', 'Kenya'),
                                    ('RW', 'Rwanda'),
                                    ('UG', 'Uganda'),
                                    ('NG', 'Nigeria'),
                                    ('ET', 'Ethiopia'),
                                    ('TZ', 'Tanzania'),
                                )],
                                default='KE')

    def __str__(self):
        return self.serial_number

class ImplementHistory(models.Model):
    implement_serial = models.ForeignKey(Implement, on_delete=models.CASCADE, related_name='history_records')  # Changed related_name
    initial_device = models.ForeignKey(Device, related_name='initial_implements', on_delete=models.SET_NULL, null=True)
    current_device = models.ForeignKey(Device, related_name='current_implements', on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    days_used = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.end_date:
            self.days_used = (self.end_date - self.start_date).days
        else:
            self.days_used = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.implement_serial.serial_number} history"

    class Meta:
        unique_together = ('implement_serial', 'start_date')

class Hub(models.Model):
    id = models.AutoField(primary_key=True)
    hub_device_imei = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='hubs')
    hub_name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(max_length=100, default=timezone.now)
    hub_location = models.CharField(max_length=100,
                                    choices=[(loc, loc) for loc in (
                                        'Kisumu',
                                        'Nakuru',
                                        'Nairobi',
                                    )],
                                    default='Kisumu')

    def __str__(self):
        return self.hub_name

class HubImplement(models.Model):
    hub_implement_serial = models.ForeignKey(Implement, on_delete=models.CASCADE, related_name='hub_history')
    implement_type = models.CharField(max_length=100, null=False, blank=False)
    attached_beacon = models.OneToOneField(Beacon, on_delete=models.CASCADE, related_name='hub_implement')
    hub_name = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='hub_implements')
    created_at = models.DateTimeField(max_length=100, default=timezone.now)

    def __str__(self):
        return f"Implement {self.hub_implement_serial.serial_number} - {self.hub_name}"
