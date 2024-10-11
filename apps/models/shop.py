from django.db.models import Model, TextField, ImageField, DateField, BooleanField, CharField, ForeignKey, CASCADE, \
    TextChoices, IntegerField
from django.utils.translation import gettext_lazy as _

from apps.models.base import TimeBasedModel


class Concurs(Model):
    description = TextField(verbose_name=_('Description'), null=True, blank=True)
    photo = ImageField(verbose_name=_('Photo'), upload_to='concurs/%Y/%m/%d')
    start_date = DateField(verbose_name=_('Start date'))
    end_date = DateField(verbose_name=_('End date'))
    is_active = BooleanField(verbose_name=_('Is active'), default=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Competition')
        verbose_name_plural = _('Competitions')


class Transaction(TimeBasedModel):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        RETURNED = 'returned', 'Returned'
        CANCELLED = 'canceled', 'Canceled'
        DISPUTED = 'disputed', 'Disputed'
        EXPIRED = 'expired', 'Expired'
        ON_HOLD = 'on_hold', 'On_hold'

    card_number = CharField(verbose_name=_('Account number'), max_length=200)
    status = CharField(verbose_name=_('Status'), max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = IntegerField(verbose_name=_('Amount'))
    message = TextField(verbose_name=_('Message'), null=True, blank=True)
    photo = ImageField(verbose_name=_('Photo'), upload_to='transactions/%Y/%m/%d', null=True, blank=True)
    owner = ForeignKey('apps.User', CASCADE, verbose_name=_('Owner'))
    is_payed = BooleanField(verbose_name=_('Is payed'), default=False)
