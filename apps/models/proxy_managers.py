from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager

User = get_user_model()


class OperatorUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.OPERATOR)


class AdminUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.ADMIN)


class ManagerUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.MANAGER)


class CustomerUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.CUSTOMER)


class CurrierUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.CURRIER)
