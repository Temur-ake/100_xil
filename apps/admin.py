from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm

admin.site.login_form = CustomAdminAuthenticationForm

from apps.models import Category, SiteSettings, AdminUserProxy, OperatorUserProxy, Order, Product, User, Concurs, \
    Operator
from apps.models.proxy import CustomerUserProxy, CurrierUserProxy, NewOrderProxy, ArchivedOrderProxy, \
    ReadyToDeliverOrderProxy, DeliveringOrderProxy, DeliveredOrderProxy, BrokenOrderProxy, ReturnedOrderProxy, \
    CanceledOrderProxy, WaitingOrderProxy


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
            'apps/js/custom.js'
        )

    def save_model(self, request, obj, form, change):
        obj.type = self._type
        super().save_model(request, obj, form, change)


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
class UserModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'


@admin.register(AdminUserProxy)
class AdminUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type'
    _type = User.Type.ADMIN


class OperatorStackedInline(StackedInline):
    model = Operator


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
    _type = User.Type.CURRIER


@admin.register(Order)
class OrderModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(NewOrderProxy)
class NewOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(ArchivedOrderProxy)
class ArchivedOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(ReadyToDeliverOrderProxy)
class ReadyToDeliverOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(DeliveringOrderProxy)
class DeliveringOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(DeliveredOrderProxy)
class DeliveredOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(BrokenOrderProxy)
class BrokenOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(ReturnedOrderProxy)
class ReturnedOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(CanceledOrderProxy)
class CanceledOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(WaitingOrderProxy)
class WaitingOrderProxyModelAdmin(ModelAdmin):
    list_display = ['phone']
    ordering = ['phone']


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    pass


@admin.register(Concurs)
class ConcursAdmin(admin.ModelAdmin):
    pass
