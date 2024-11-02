from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.models import Transaction


@receiver(post_save, sender=Transaction)
def subtract_from_user_balance(sender, instance: Transaction, **kwargs):
    if instance.status == Transaction.Status.COMPLETED and not instance.is_payed:
        transaction_owner = instance.owner
        transaction_owner.balance -= instance.amount
        transaction_owner.save()
        instance.is_payed = True
        instance.save()
