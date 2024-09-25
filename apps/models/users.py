from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, BigIntegerField, TextChoices, Model, ForeignKey, CASCADE, \
    PositiveIntegerField, ImageField

from apps.models.managers import CustomUserManager


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
        OPERATOR = 'operator', 'Operator'
        CURRIER = 'currier', 'Kuryer'

    email = None
    username = None
    phone = CharField(max_length=20, unique=True)
    photo = ImageField(upload_to='users/%Y/%m/%d', default='default_active_user.jpg', null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    about = TextField(null=True, blank=True)
    telegram_id = BigIntegerField(unique=True, null=True, blank=True)
    type = CharField(max_length=15, choices=Type.choices, default=Type.USER)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


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


class SiteSettings(Model):
    fee_for_operator = PositiveIntegerField(blank=True, default=4000)
    fee_for_currier = PositiveIntegerField(blank=True, default=10000)
    concurs_photo = ImageField(upload_to='concurs/%Y/%m/%d', null=True, blank=True)
    tashkent_city = PositiveIntegerField(blank=True, default=20000)
    tashkent_region = PositiveIntegerField(blank=True, default=25000)
    other_regions = PositiveIntegerField(blank=True, default=35000)


'''
operator (3000)
referral user (30000)
currier
dostovka narxi (toshkent shahar) 20000
dostovka narxi (toshkent vil) 25000
dostovka narxi (viloyatga) 30000


kiyim narxi  160,000 so'm

oqim orqali 40,000 so'm

'''
