from django.db.models import PositiveIntegerField, ImageField, CharField, ForeignKey, CASCADE, Model, TextChoices
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import TimeSlugBased, TimeBasedModel


class Product(TimeSlugBased):
    price = PositiveIntegerField(help_text="So'mda")
    photo = ImageField(upload_to='products/%Y/%m/%d')
    quantity = PositiveIntegerField()
    discount = CharField(max_length=255, null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE)
    description = CKEditor5Field()


class Order(TimeBasedModel):
    class Status(TextChoices):
        NEW = 'new', 'New'
        READY_TO_DELIVER = 'ready_to_deliver', 'Ready_to_deliver'
        DELIVERING = 'delivering', 'Delivering'
        DELIVERED = 'delivered', 'Delivered'
        CANT_PHONE = 'cant_phone', 'Cant_phone'
        CANCELED = 'canceled', 'Canceled'
        ARCHIVED = 'archived', 'Archived'

    quantity = PositiveIntegerField(default=1, null=True, blank=True)
    status = CharField(max_length=50, choices=Status.choices, default=Status.NEW)
    full_name = CharField(max_length=50)
    phone = CharField(max_length=20)
    stream = ForeignKey('apps.Stream', CASCADE, null=True, blank=True)
    product = ForeignKey('apps.Product', CASCADE)
    owner = ForeignKey('apps.User', CASCADE)


class Stream(TimeBasedModel):
    name = CharField(max_length=255)
    discount = PositiveIntegerField()
    product = ForeignKey('apps.Product', CASCADE)
    owner = ForeignKey('apps.User', CASCADE)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class Wishlist(Model):
    product = ForeignKey('apps.Product', CASCADE)
    owner = ForeignKey('apps.User', CASCADE)
