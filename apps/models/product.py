from django.db.models import PositiveIntegerField, ImageField, CharField, ForeignKey, CASCADE, TextChoices, TextField, \
    DateTimeField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import TimeSlugBased, TimeBasedModel


class Product(TimeSlugBased):
    price = PositiveIntegerField(help_text="So'mda")
    photo = ImageField(upload_to='products/%Y/%m/%d')
    quantity = PositiveIntegerField()
    discount = CharField(max_length=255, null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE)
    description = CKEditor5Field()
    product_fee = PositiveIntegerField(help_text="So'mda", null=True, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Order(TimeBasedModel):
    class Status(TextChoices):
        NEW = 'new', 'New'
        ARCHIVED = 'archived', 'Archived'
        READY_TO_DELIVER = 'ready_to_deliver', 'Ready to deliver'
        DELIVERING = 'delivering', 'Delivering'
        DELIVERED = 'delivered', 'Delivered'
        BROKEN = 'broken', 'Broken'
        RETURNED = 'returned', 'Returned'
        CANCELED = 'canceled', 'Canceled'
        WAITING = 'waiting', 'Waiting'

    quantity = PositiveIntegerField(db_default=1)
    status = CharField(max_length=50, choices=Status.choices, default=Status.NEW)
    full_name = CharField(max_length=50, null=True, blank=True)
    phone = CharField(max_length=20)
    stream = ForeignKey('apps.Stream', CASCADE, null=True, blank=True, related_name='orders')
    product = ForeignKey('apps.Product', CASCADE, related_name='orders')
    owner = ForeignKey('apps.User', CASCADE, null=True, blank=True)
    operator = ForeignKey('apps.User', CASCADE, null=True, blank=True, related_name='operator_orders')
    currier = ForeignKey('apps.User', CASCADE, null=True, blank=True, related_name='currier_orders')
    region = ForeignKey('apps.Region', CASCADE, null=True, blank=True)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True)
    comment = TextField(null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    send_date = DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class Stream(TimeBasedModel):
    name = CharField(max_length=255)
    discount = PositiveIntegerField(db_default=0, null=True, blank=True)
    visit_count = PositiveIntegerField(db_default=0)
    product = ForeignKey('apps.Product', CASCADE)
    owner = ForeignKey('apps.User', CASCADE)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name

    @property
    def changed_price(self):
        return self.product.price - self.discount
