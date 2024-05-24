from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, CustomUser


@receiver(post_save, sender=CustomUser)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance,
                                email=instance.email,
                                username=instance.last_name)


@receiver(post_save, sender=CustomUser)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()
