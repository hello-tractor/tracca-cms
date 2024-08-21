from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class live_tracking_data(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    device_id = models.IntegerField(editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    speed = models.FloatField(default=0.0)
    fuel_frequency = models.FloatField(null=True, blank=True)
    position = models.CharField(max_length=255, default=0.0)
    engine_state = models.CharField(max_length=50, null=True, blank=True)
    asset_battery = models.FloatField(null=True, blank=True)
    raw_value = models.CharField(max_length=255, null=True, blank=True)
    sim_iccid = models.CharField(max_length=100, null=True, blank=True)
    other_data = models.JSONField()

    def __str__(self):
        return f"Device {self.device_id} - {self.latitude}, {self.longitude}"

class Device(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
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

class Hub(models.Model):
    id = models.AutoField(primary_key=True)
    hub_device_imei = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='hubs')
    hub_name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    hub_location = models.CharField(max_length=100,
                                    choices=[(loc, loc) for loc in (
                                        'Kisumu',
                                        'Nakuru',
                                        'Nairobi',
                                    )],
                                    default='Kisumu')

    def __str__(self):
        return self.hub_name

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
    device_id = models.CharField(max_length=100, unique=True, editable=False)
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the 'is_within_hub' status for related HubImplements
        hub_implements = HubImplement.objects.filter(attached_beacon_id=self)
        for hub_implement in hub_implements:
            hub_implement.update_is_within_hub()

class Implement(models.Model):
    serial_number = models.CharField(max_length=100, primary_key=True, blank=False, default=None)
    brand = models.ForeignKey(ImplementBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    attached_beacon_id = models.OneToOneField(Beacon, on_delete=models.CASCADE, related_name='implement')
    created_at = models.DateTimeField(default=timezone.now)
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
    associated_with_hub = models.BooleanField(default=False)  # New flag field
    hub = models.ForeignKey(Hub, on_delete=models.SET_NULL, null=True, blank=True)  # New hub field

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Implement first
        if self.associated_with_hub and self.hub:
            # Create or update the corresponding HubImplement
            HubImplement.objects.update_or_create(
                implement=self,
                defaults={
                    'hub': self.hub,
                    'serial_number': self.serial_number,
                    'brand': self.brand,
                    'model': self.model,
                    'color': self.color,
                    'attached_beacon_id': self.attached_beacon_id,
                    'created_at': self.created_at,
                    'location': self.location,
                    'is_within_hub': False,  # This will be updated dynamically based on beacons
                }
            )

    def __str__(self):
        return self.serial_number

class ImplementHistory(models.Model):
    implement_serial = models.ForeignKey(Implement, on_delete=models.CASCADE, related_name='history_records')
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

class HubImplement(models.Model):
    hub = models.ForeignKey('Hub', on_delete=models.CASCADE, related_name='hub_implements', editable=False)
    
    # Fields from Implement, with appropriate defaults
    serial_number = models.CharField(max_length=100, default="UNKNOWN_SERIAL", editable=False)
    brand = models.ForeignKey('ImplementBrand', on_delete=models.CASCADE, default=1, editable=False)
    model = models.CharField(max_length=100, default="UNKNOWN_MODEL", editable=False)
    color = models.CharField(max_length=50, default="UNKNOWN_COLOR", editable=False)
    attached_beacon_id = models.OneToOneField('Beacon', on_delete=models.CASCADE, editable=False, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    location = models.CharField(
        max_length=100, 
        choices=[
            ('KE', 'Kenya'),
            ('RW', 'Rwanda'),
            ('UG', 'Uganda'),
            ('NG', 'Nigeria'),
            ('ET', 'Ethiopia'),
            ('TZ', 'Tanzania'),
        ], 
        default="UNKNOWN_LOCATION", 
        editable=False
    )

    # Additional fields specific to HubImplement
    is_within_hub = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"Hub: {self.hub.hub_name} - Serial: {self.serial_number}"

    class Meta:
        verbose_name = "Hub Implement"
        verbose_name_plural = "Hub Implements"
    
    def update_is_within_hub(self):
        """
        Check if the implement's beacon is detected by the hub's device.
        """
        hub_device = self.hub.hub_device_imei
        beacons_detected_by_hub = Beacon.objects.filter(attached_to=hub_device.device_imei)
        
        if self.attached_beacon_id in beacons_detected_by_hub:
            self.is_within_hub = True
        else:
            self.is_within_hub = False
        self.save()


class FuelCalibrationResult(models.Model):
    device = models.ForeignKey(Device, related_name='calibration_results', on_delete=models.CASCADE)
    fuel_in_litre = models.FloatField()
    raw_fuel_value = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Calibration for {self.device.name} - {self.fuel_in_litre}L: {self.raw_fuel_value}"

class RealTimeFuelValue(models.Model):
    device = models.ForeignKey(Device, related_name='real_time_fuel_values', on_delete=models.CASCADE)
    computed_value = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def compute_fuel_value(self):
        calibration_results = self.device.calibration_results.all()
        if calibration_results.exists():
            # Use linear regression or similar method to compute the value
            # For simplicity, we'll just average the values here
            total_fuel = sum([res.fuel_in_litre for res in calibration_results])
            total_value = sum([res.raw_fuel_value for res in calibration_results])
            self.computed_value = total_value / total_fuel  # Replace with actual computation
        else:
            raise ValidationError("No calibration data available for this device.")

    def save(self, *args, **kwargs):
        self.compute_fuel_value()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Real-time Fuel Value for {self.device.name}: {self.computed_value}"
