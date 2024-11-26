from django.utils.translation import gettext_lazy as _

from apps.models import User, Order
from apps.models.proxy_managers import OperatorUserManager, AdminUserManager, CustomerUserManager, CurrierUserManager, \
    ManagerUserManager


class OperatorUserProxy(User):
    objects = OperatorUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')


class OperatorStatisticUserProxy(User):
    objects = OperatorUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Operator Statistics')
        verbose_name_plural = _('Operators Statistics')


class CurrierStatisticUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Currier Statistics')
        verbose_name_plural = _('Currier Statistics')


class FreshCurrierStatisticUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Fresh food Kurrierlar Statistikasi')
        verbose_name_plural = _('Fresh food Kurrierlar Statistikasi')


class AdminUserProxy(User):
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')


class ManagerUserProxy(User):
    objects = ManagerUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')


class CustomerUserProxy(User):
    objects = CustomerUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class CurrierUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Currier')
        verbose_name_plural = _('Curriers')


class NewOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('New')
        verbose_name_plural = _('New')


class DeliveringOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Delivering')
        verbose_name_plural = _('Delivering')


class DeliveredOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Delivered')
        verbose_name_plural = _('Delivered')


class FreshStatisticProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Fresh food Statistikasi'
        verbose_name_plural = 'Fresh food Statistikalari'


class FreshfoodKuryerlari(User):
    class Meta:
        proxy = True
        verbose_name = 'Fresh food Kuryerlari'
        verbose_name_plural = 'Fresh food Kuryerlari'

# class BrokenOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = _('Broken')
#         verbose_name_plural = _('Broken')
#
#
# class ReturnedOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = _('Returned')
#         verbose_name_plural = _('Returned')
#
#
# class CanceledOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = _('Canceled')
#         verbose_name_plural = _('Canceled')
#
#
# class WaitingOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = _('Waiting')
#         verbose_name_plural = _('Waiting')

# class ArchivedOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = _('Archived')
#         verbose_name_plural = _('Archived')
#
#
# class ReadyToDeliverOrderProxy(Order):
#     class Meta:
#         proxy = True
#         verbose_name = _('Ready')
#         verbose_name_plural = _('Readies')
