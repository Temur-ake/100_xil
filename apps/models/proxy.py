from django.utils.translation import gettext_lazy as _

from apps.models import User, Order
from apps.models.proxy_managers import AdminUserManager, CustomerUserManager, CurrierUserManager, \
    ManagerUserManager


#


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


class MyBiznesStatisticProxy(Order):
    class Meta:
        proxy = True
        verbose_name = 'Biznes Statistikasi'
        verbose_name_plural = 'Biznes Statistikalari'


class BarchaKuryerlarStatistikasiUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Barcha Kuryerlar Statistikasi')
        verbose_name_plural = _('Barcha Kuryerlar Statistikasi')


class MeningKuryerlarimStatistikasiUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Mening Kuryerlarim Statistikasi ')
        verbose_name_plural = _('Mening Kuryerlarim Statistikasi ')


class MeningKuryerlarimUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Mening Kuryerlarim')
        verbose_name_plural = _('Mening Kuryerlarim')


class BarchaKuryerlarUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Barcha Kurrierlar')
        verbose_name_plural = _('Barcha Kurrierlar')


class UmumiyRaqamlarProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('UmumiyRaqamlar')
        verbose_name_plural = _('UmumiyRaqamlar')

# class FreshfoodKuryerlari(User):
#     class Meta:
#         proxy = True
#         verbose_name = 'Fresh food Kuryerlari'
#         verbose_name_plural = 'Fresh food Kuryerlari'

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


# class OperatorUserProxy(User):
#     objects = OperatorUserManager()
#
#     class Meta:
#         proxy = True
#         verbose_name = _('Operator')
#         verbose_name_plural = _('Operators')
#
#
# class OperatorStatisticUserProxy(User):
#     objects = OperatorUserManager()
#
#     class Meta:
#         proxy = True
#         verbose_name = _('Operator Statistics')
#         verbose_name_plural = _('Operators Statistics')
