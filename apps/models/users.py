from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, BigIntegerField, TextChoices, Model, ForeignKey, CASCADE, \
    PositiveIntegerField, ImageField, OneToOneField, TimeField, IntegerField
from django.utils.translation import gettext_lazy as _

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        CUSTOMER = 'customer', 'Customer'
        OPERATOR = 'operator', 'Operator'
        CURRIER = 'currier', 'Currier'

    email = None
    username = None
    phone = CharField(max_length=20, unique=True)
    photo = ImageField(upload_to='users/%Y/%m/%d', default='default_active_user.jpg', null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    about = TextField(null=True, blank=True)
    telegram_id = BigIntegerField(unique=True, null=True, blank=True)
    type = CharField(max_length=15, choices=Type.choices, default=Type.CUSTOMER)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True)
    balance = IntegerField(null=True, blank=True, default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    # def clean_fields(self, exclude=None):
    #     self.phone = re.sub(r'[^\d]', '', self.phone)
    #     if len(self.phone) > 9:
    #         self.phone = self.phone[-9:]
    #
    #     if len(self.phone) != 9:
    #         raise ValidationError('Nomer xatoku')
    #
    #     return super().clean_fields(exclude)

    def is_operator(self):
        return self.type == self.Type.OPERATOR

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Operator(Model):
    user = OneToOneField('apps.User', CASCADE)
    passport_number = CharField(verbose_name='Passport raqami', max_length=20)
    start_work_time = TimeField(verbose_name='Ish boshlash vaqti')
    end_work_time = TimeField(verbose_name='Ish tugash vaqti')

    def __str__(self):
        return f"{self.user.username} - Operator"


class Region(Model):
    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=50)
    region = ForeignKey('apps.Region', CASCADE)

    def __str__(self):
        return self.name


class SpamUser(Model):
    phone = CharField(max_length=20, unique=True)
    user = ForeignKey('apps.User', CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Spam')
        verbose_name_plural = _('Spams')


class SiteSettings(Model):
    fee_for_operator = PositiveIntegerField(blank=True, default=4000)
    fee_for_currier = PositiveIntegerField(blank=True, default=10000)
    tashkent_city = PositiveIntegerField(blank=True, default=20000)
    tashkent_region = PositiveIntegerField(blank=True, default=25000)
    other_regions = PositiveIntegerField(blank=True, default=35000)
    min_balance_amount = IntegerField(default=100000)

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
