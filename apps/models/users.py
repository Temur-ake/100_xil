import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import CharField, TextField, BigIntegerField, TextChoices, Model, ForeignKey, CASCADE, \
    PositiveIntegerField, ImageField, OneToOneField, TimeField, IntegerField
from django.utils.translation import gettext_lazy as _

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        CUSTOMER = 'customer', _('Customer')
        OPERATOR = 'operator', 'Operator'
        CURRIER = 'currier', 'Currier'

    email = None
    username = None
    phone = CharField(verbose_name=_('Phone'), max_length=20, unique=True)
    photo = ImageField(verbose_name=_('Photo'), upload_to='users/%Y/%m/%d', default='default_active_user.jpg',
                       null=True, blank=True)
    address = CharField(verbose_name=_('Address'), max_length=255, null=True, blank=True)
    about = TextField(verbose_name=_('About user'), null=True, blank=True)
    telegram_id = BigIntegerField(verbose_name=_('Telegram ID'), unique=True, null=True, blank=True)
    type = CharField(verbose_name=_('Type'), max_length=15, choices=Type.choices, default=Type.CUSTOMER)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True, verbose_name=_('District'))
    balance = IntegerField(verbose_name=_('Balance'), null=True, blank=True, default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def clean_fields(self, exclude=None):
        self.phone = re.sub(r'[^\d]', '', self.phone)
        if len(self.phone) > 9:
            self.phone = self.phone[-9:]

        if len(self.phone) != 9:
            raise ValidationError(_('Incorrect phone number'))

        return super().clean_fields(exclude)

    def is_operator(self):
        return self.type == self.Type.OPERATOR

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Operator(Model):
    user = OneToOneField('apps.User', CASCADE, limit_choices_to={'type': User.Type.OPERATOR})
    passport_number = CharField(verbose_name=_('Passport number'), max_length=20)
    start_work_time = TimeField(verbose_name=_('Start work time'))
    end_work_time = TimeField(verbose_name=_('End work time'))

    def __str__(self):
        return f"{self.user.username} - Operator"


class Currier(Model):
    user = OneToOneField('apps.User', CASCADE, limit_choices_to={'type': User.Type.CURRIER})
    region = ForeignKey('apps.Region', CASCADE, verbose_name=_('Region'))
    district = ForeignKey('apps.District', CASCADE, verbose_name=_('District'))

    def __str__(self):
        return f"{self.user.username} - Currier"


class Region(Model):
    name = CharField(verbose_name=_('Name'), max_length=50)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(verbose_name=_('Name'), max_length=50)
    region = ForeignKey('apps.Region', CASCADE, verbose_name=_('Region'))

    def __str__(self):
        return self.name


class SpamUser(Model):
    phone = CharField(verbose_name=_('Phone'), max_length=20, unique=True)
    user = ForeignKey('apps.User', CASCADE, null=True, blank=True, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Spam')
        verbose_name_plural = _('Spams')


class SiteSettings(Model):
    fee_for_operator = PositiveIntegerField(verbose_name=_('Operator fee'), blank=True, default=4000)
    fee_for_currier = PositiveIntegerField(verbose_name=_('Currier fee'), blank=True, default=10000)
    tashkent_city = PositiveIntegerField(verbose_name=_('Delivery price for Tashkent city'), blank=True, default=20000)
    tashkent_region = PositiveIntegerField(verbose_name=_('Delivery price for Tashkent region'), blank=True,
                                           default=25000)
    other_regions = PositiveIntegerField(verbose_name=_('Delivery price for other regions'), blank=True, default=35000)
    min_balance_amount = IntegerField(verbose_name=_('Minimum amount for withdraw'), default=100000)

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
