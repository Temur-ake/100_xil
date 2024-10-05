from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Order


@receiver(post_save, sender=Order)
def update_balance_on_delivery(sender, instance: Order, **kwargs):
    if instance.stream and instance.status == Order.Status.DELIVERED and not instance.is_product_fee_added:
        stream_owner = instance.stream.owner
        stream_owner.balance += instance.product.product_fee
        instance.is_product_fee_added = True
        instance.save()
        stream_owner.save()
