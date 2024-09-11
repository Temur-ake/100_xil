from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField, BigIntegerField, TextChoices, Model, ForeignKey, CASCADE

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
