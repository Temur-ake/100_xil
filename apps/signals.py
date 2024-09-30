from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Order


@receiver(post_save, sender=Order)
def update_balance_on_delivery(sender, instance: Order, **kwargs):
    if instance.stream and instance.status == Order.Status.DELIVERED:
        stream_owner = instance.stream.owner
        stream_owner.balance += instance.product.product_fee
        stream_owner.save()