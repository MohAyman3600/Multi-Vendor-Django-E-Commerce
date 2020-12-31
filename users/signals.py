"""Signals for user and profile models."""
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='users.VendorProfile')
def set_user_to_vendor(sender, instance, **kwargs):
    """Set the user is_vendor attribut to True when VendorProfile is saved."""
    instance.user.is_vendor = True
    instance.user.save()


@receiver(post_save, sender='users.CustomerProfile')
def set_user_to_customer(sender, instance, **kwargs):
    """Set the user is_vendor attribut to True when CustomerProfile is saved."""
    instance.user.is_customer = True
    instance.user.save()
