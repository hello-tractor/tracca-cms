from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from .models import Device, Implement, ImplementHistory

@receiver(post_save, sender=Device)
def update_implement_history(sender, instance, **kwargs):
    if instance.active_implement:
        try:
            implement = Implement.objects.get(serial_number=instance.active_implement)
        except Implement.DoesNotExist:
            return

        # Check for the current history record
        current_history = ImplementHistory.objects.filter(
            implement_serial=implement,
            current_device=instance
        ).last()

        if current_history and current_history.current_device == instance:
            # Update the end_date if the implement is still with the same device
            current_history.end_date = None
            current_history.save()
        else:
            # Close the current history record if it exists and the device has changed
            if current_history:
                current_history.end_date = timezone.now()
                current_history.save()

            # Create a new history record
            ImplementHistory.objects.create(
                implement_serial=implement,
                initial_device=instance,
                current_device=instance,
                start_date=timezone.now(),
            )
