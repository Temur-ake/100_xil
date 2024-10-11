from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm

admin.site.login_form = CustomAdminAuthenticationForm

from apps.models import Category, SiteSettings, AdminUserProxy, OperatorUserProxy, Order, Product, User, Concurs, \
    Operator, Transaction, Currier
from apps.models.proxy import CustomerUserProxy, CurrierUserProxy, NewOrderProxy, ArchivedOrderProxy, \
    ReadyToDeliverOrderProxy, DeliveringOrderProxy, DeliveredOrderProxy, BrokenOrderProxy, ReturnedOrderProxy, \
    CanceledOrderProxy, WaitingOrderProxy


def get_app_list(self, request, app_label=None):
    ordering = {
        'Order': 1,
        'NewOrderProxy': 2,
        'ArchivedOrderProxy': 3,
        'ReadyToDeliverOrderProxy': 4,
        'DeliveringOrderProxy': 5,
        'DeliveredOrderProxy': 6,
        'BrokenOrderProxy': 7,
        'ReturnedOrderProxy': 8,
        'CanceledOrderProxy': 9,
        'WaitingOrderProxy': 10,
        'Category': 11,
        'Product': 12,
        'User': 13,
        'AdminUserProxy': 14,
        'OperatorUserProxy': 15,
        'CustomerUserProxy': 16,
        'CurrierUserProxy': 17,
        'SiteSettings': 18,
        'Concurs': 19,
        'Transaction': 20
    }
    app_dict = self._build_app_dict(request)

    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    for app in app_list:
        app['models'].sort(key=lambda x: ordering[x['object_name']])

    return app_list


admin.AdminSite.get_app_list = get_app_list


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('phone', "usable_password", "password1", "password2"),
            },
        ),
    )

    ordering = ['phone']
    list_display = ['phone']

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/currier_custom.js'
        )

    def save_model(self, request, obj, form, change):
        obj.type = self._type
        super().save_model(request, obj, form, change)


class CustomModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/custom.js'
        )


@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'id', 'name', 'price', 'quantity', 'gfvhb'
    list_display_links = 'name',

    @admin.display(description='Rasmi')
    def gfvhb(self, obj: Product):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None'


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('phone', "usable_password", "password1", "password2"),
            },
        ),
    )

    ordering = ['phone']
    list_display = ['phone']

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/custom.js'
        )


@admin.register(AdminUserProxy)
class AdminUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'
    _type = User.Type.ADMIN


class OperatorStackedInline(StackedInline):
    model = Operator


class CurrierStackedInline(StackedInline):
    model = Currier


@admin.register(OperatorUserProxy)
class OperatorUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'
    _type = User.Type.OPERATOR
    inlines = [OperatorStackedInline]


@admin.register(CustomerUserProxy)
class CustomerUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'
    _type = User.Type.CUSTOMER


@admin.register(CurrierUserProxy)
class CurrierUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'
    inlines = [CurrierStackedInline]
    _type = User.Type.CURRIER


@admin.register(Order)
class OrderModelAdmin(CustomModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'address', 'stream'
    list_display_links = 'status',
    list_filter = 'id', 'phone'


@admin.register(NewOrderProxy)
class NewOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.NEW)


@admin.register(ArchivedOrderProxy)
class ArchivedOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.ARCHIVED)


@admin.register(ReadyToDeliverOrderProxy)
class ReadyToDeliverOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.READY_TO_DELIVER)


@admin.register(DeliveringOrderProxy)
class DeliveringOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.DELIVERING)


@admin.register(DeliveredOrderProxy)
class DeliveredOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.DELIVERED)


@admin.register(BrokenOrderProxy)
class BrokenOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.BROKEN)


@admin.register(ReturnedOrderProxy)
class ReturnedOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.RETURNED)


@admin.register(CanceledOrderProxy)
class CanceledOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.CANCELED)


@admin.register(WaitingOrderProxy)
class WaitingOrderProxyModelAdmin(OrderModelAdmin):

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.WAITING)


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    pass


@admin.register(Concurs)
class ConcursAdmin(admin.ModelAdmin):
    list_display = 'start_date', 'end_date', 'is_active', 'photo_'
    list_display_links = 'start_date', 'end_date'

    @admin.display(description='Photo')
    def photo_(self, obj: Concurs):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None image'

    def message_user(self, request, message, level=messages.INFO, extra_tags="", fail_silently=False):
        pass

    def save_model(self, request, obj, form, change):
        if (obj.id is None and obj.is_active) and Concurs.objects.filter(is_active=True).exists():
            messages.add_message(request, messages.WARNING, 'Already exists active competition✋')
            return
        messages.add_message(request, messages.INFO,
                             f'The Konkurs was {obj.description} added successfully.')
        super().save_model(request, obj, form, change)


@admin.register(Transaction)
class TransactionModelAdmin(ModelAdmin):
    list_display = 'status', 'amount', 'message', 'bill_photo', 'owner'
    list_display_links = 'amount',

    @admin.display(description='Photo')
    def bill_photo(self, obj: Transaction):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None image'


admin.site.unregister(Group)
