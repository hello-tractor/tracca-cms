from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Beacon, ImplementHistory, Device

@receiver(post_save, sender=Beacon)
def create_or_update_beacon_history(sender, instance, **kwargs):
    try:
        current_device = Device.objects.get(id=instance.device_id)  # Fetch the current device
    except Device.DoesNotExist:
        return  # Handle the case where the device is not found

    # Check if there's an existing BeaconHistory record for this beacon and device
    history, created = ImplementHistory.objects.get_or_create(
        beacon=instance,
        defaults={'device': current_device, 'start_time': instance.attached_time}
    )

    if not created:
        # If the record already exists, check if the device has changed
        if history.device != current_device:
            history.device = current_device
            history.start_time = instance.attached_time  # Reset start time
            history.save()
