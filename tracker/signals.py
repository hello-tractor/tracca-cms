from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import TractorDetails, Implement, OwnershipHistory
from .middleware import get_current_user

@receiver(pre_save, sender=TractorDetails)
def update_updated_by_tractor(sender, instance, **kwargs):
    current_user = get_current_user()
    if current_user:
        instance.updated_by = current_user

@receiver(post_save, sender=TractorDetails)
def create_ownership_history_tractor(sender, instance, created, **kwargs):
    if not created:
        current_user = get_current_user()
        previous_owner = sender.objects.get(pk=instance.pk).owner
        if instance.owner != previous_owner:
            OwnershipHistory.objects.create(
                tractor=instance,
                previous_owner=previous_owner,
                new_owner=instance.owner,
                updated_by=current_user
            )

@receiver(pre_save, sender=Implement)
def update_updated_by_implement(sender, instance, **kwargs):
    current_user = get_current_user()
    if current_user:
        instance.updated_by = current_user

@receiver(post_save, sender=Implement)
def create_ownership_history_implement(sender, instance, created, **kwargs):
    if not created:
        current_user = get_current_user()
        previous_owner = sender.objects.get(pk=instance.pk).owner
        if instance.owner != previous_owner:
            OwnershipHistory.objects.create(
                implement=instance,
                previous_owner=previous_owner,
                new_owner=instance.owner,
                updated_by=current_user
            )
