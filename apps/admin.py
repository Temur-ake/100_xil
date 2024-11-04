from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count, F, Q, DateTimeField, Min, Max
from django.db.models.functions import TruncMonth
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm
from apps.views.auth_views import SuccessValijonTemplateView

admin.site.login_form = CustomAdminAuthenticationForm

from apps.models import Category, SiteSettings, AdminUserProxy, OperatorUserProxy, Order, Product, User, Concurs, \
    Operator, Transaction, OperatorStatisticUserProxy, District
from apps.models.proxy import CustomerUserProxy, CurrierUserProxy, NewOrderProxy, ArchivedOrderProxy, \
    ReadyToDeliverOrderProxy, DeliveringOrderProxy, DeliveredOrderProxy, BrokenOrderProxy, ReturnedOrderProxy, \
    CanceledOrderProxy, WaitingOrderProxy, ManagerUserProxy


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request)

    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
    if not request.user.is_superuser:
        return app_list
    all_models = app_list[0].pop('models')
    app_list[0]['models'] = list()

    new_apps = {
        'label': {
            'name': _("Users"),
            "app_label": 'label',
            'models': list()
        },
        'label2': {
            'name': _("Orders"),
            "app_label": 'label25',
            'models': list()
        },
        'label3': {
            'name': _("Alijahon-Shop"),
            "app_label": 'label3',
            'models': list()
        }
    }

    model_order = {
        'Order': 'label2',
        'NewOrderProxy': 'label2',
        'ArchivedOrderProxy': 'label2',
        'ReadyToDeliverOrderProxy': 'label2',
        'DeliveringOrderProxy': 'label2',
        'DeliveredOrderProxy': 'label2',
        'BrokenOrderProxy': 'label2',
        'ReturnedOrderProxy': 'label2',
        'CanceledOrderProxy': 'label2',
        'WaitingOrderProxy': 'label2',
        'User': 'label',
        'AdminUserProxy': 'label',
        'ManagerUserProxy': 'label',
        'OperatorUserProxy': 'label',
        'OperatorStatisticUserProxy': 'label',
        'CustomerUserProxy': 'label',
        'CurrierUserProxy': 'label',
        'Category': 'label3',
        'Product': 'label3',
        'SiteSettings': 'label3',
        'Concurs': 'label3',
        'Transaction': 'label3'
    }

    for _model in all_models:
        if _model['object_name'] in model_order.keys():
            new_apps[model_order[_model['object_name']]]['models'].append(_model)
        else:
            app_list[0]['models'].append(_model)
    if not app_list[0]['models']:
        return list(new_apps.values())
    app_list.extend(new_apps.values())
    return app_list


admin.AdminSite.get_app_list = get_app_list


class CustomAdminMixin:
    def change_button(self, obj):
        change_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.id])
        return format_html("""
        <button style="background-color:#417690; padding: 10px 20px; border:none; border-radius:5px;">
            <a href="{}" style="color:white; text-decoration:none; display:inline-block;">{}</a>
        </button>
        """, change_url, _('Edit'))

    def delete_button(self, obj):
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.id])
        return format_html("""
        <button style="background-color:#ba2121; padding: 10px 20px; border:none; border-radius:5px;">
            <a href="{}" style="color:white; text-decoration:none; display:inline-block;">Delete</a>
        </button>
        """, delete_url)


class CustomUserAdmin(CustomAdminMixin, UserAdmin):
    ordering = ['phone']
    list_display = ['phone']
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", 'region', 'district', 'type', 'balance')}),
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

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/currier_custom.js'
        )

    autocomplete_fields = ['district']

    def save_model(self, request, obj, form, change):
        obj.type = self._type
        super().save_model(request, obj, form, change)

    @admin.display(description=_('Edit'))
    def change_button(self, obj):
        return super().change_button(obj)

    @admin.display(description=_('Delete'))
    def delete_button(self, obj):
        return super().delete_button(obj)

    def get_list_display_links(self, request, list_display):
        pass


class CustomModelAdmin(CustomAdminMixin, ModelAdmin):
    list_display = 'phone',
    ordering = 'phone',

    def get_urls(self):
        return [
            path(
                "valijon",
                self.admin_site.admin_view(SuccessValijonTemplateView.as_view()),
                name="valijon",
            ),
            *super().get_urls(),
        ]

    @admin.display(description=_('Edit'))
    def change_button(self, obj):
        return super().change_button(obj)

    @admin.display(description=_('Delete'))
    def delete_button(self, obj):
        return super().delete_button(obj)

    def get_list_display_links(self, request, list_display):
        pass

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/custom.js'
        )


class CustomShopModelAdmin(ModelAdmin, CustomAdminMixin):

    @admin.display(description=_('Edit'))
    def change_button(self, obj):
        return super().change_button(obj)

    @admin.display(description=_('Delete'))
    def delete_button(self, obj):
        return super().delete_button(obj)

    def get_list_display_links(self, request, list_display):
        pass


@admin.register(Category)
class CategoryModelAdmin(CustomShopModelAdmin):
    list_display = 'id', 'name', 'image', 'change_button', 'delete_button'
    search_fields = 'name',

    @admin.display(description=_('Photo'))
    def image(self, obj: Category):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")


@admin.register(Product)
class ProductModelAdmin(CustomShopModelAdmin):
    list_display = 'id', 'name', 'price', 'quantity', 'gfvhb', 'change_button', 'delete_button'
    search_fields = 'id', 'name', 'price'

    @admin.display(description=_('Photo'))
    def gfvhb(self, obj: Product):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None'


@admin.register(User)
class UserModelAdmin(UserAdmin, CustomAdminMixin):

    @admin.display(description=_('Edit'))
    def change_button(self, obj):
        return super().change_button(obj)

    @admin.display(description=_('Delete'))
    def delete_button(self, obj):
        return super().delete_button(obj)

    def get_list_display_links(self, request, list_display):
        pass

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "type", "balance")}),
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
    list_display = ['id', 'phone', 'first_name', 'last_name', 'type', 'change_button', 'delete_button']

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/custom.js'
        )


@admin.register(AdminUserProxy)
class AdminUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type', 'change_button', 'delete_button'
    _type = User.Type.ADMIN


@admin.register(ManagerUserProxy)
class ManagerUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type', 'change_button', 'delete_button'
    _type = User.Type.MANAGER


class OperatorStackedInline(StackedInline):
    model = Operator


@admin.register(OperatorUserProxy)
class OperatorUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type', 'readies', 'change_button', 'delete_button'
    _type = User.Type.OPERATOR
    inlines = OperatorStackedInline,

    @admin.display(description=_('Amount of ready to delivery'))
    def readies(self, obj: OperatorUserProxy):
        count = Order.objects.filter(Q(status=Order.Status.READY_TO_DELIVER) & Q(operator=obj)).count()
        if count > 0:
            url = reverse(f'admin:{obj._meta.app_label}_{Order._meta.model_name}_changelist')
            url += f'?status={Order.Status.READY_TO_DELIVER}&operator__id__exact={obj.id}'
            return format_html('<a href="{}">{}</a>', url, count)
        return count


@admin.register(OperatorStatisticUserProxy)
class OperatorStatisticUserProxyModelAdmin(CustomUserAdmin):
    change_list_template = 'admin/operator_statistics.html'
    _type = User.Type.OPERATOR

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('operator_orders'),
            'succeed': Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED)),
            'operator_full_name': F('first_name')
        }

        response.context_data['summary'] = list(
            qs
            .annotate(**metrics).annotate(of_total_talks=(F('succeed') * 100 / F('total')))
            .order_by('first_name')
        )
        updated_metrics = metrics
        del updated_metrics['operator_full_name']
        response.context_data['summary_total'] = dict(
            qs.aggregate(**updated_metrics)
        )

        response.context_data['overall'] = (
                response.context_data['summary_total']['succeed'] * 100 // response.context_data['summary_total'][
            'total']
        )

        summary_over_time = OperatorStatisticUserProxy.objects.filter(
            operator_orders__status=Order.Status.DELIVERED).annotate(
            period=TruncMonth('operator_orders__created_at', output_field=DateTimeField())
        ).values('period').annotate(
            total=Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED))).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
                ((x['total'] or 0) - low) / (high - low) * 100
                if high > low else 0,
        } for x in summary_over_time]

        return response


@admin.register(District)
class DistrictModelAdmin(ModelAdmin):
    search_fields = 'name',


@admin.register(CustomerUserProxy)
class CustomerUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type', 'change_button', 'delete_button'
    _type = User.Type.CUSTOMER


@admin.register(CurrierUserProxy)
class CurrierUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'type', 'change_button', 'delete_button'
    _type = User.Type.CURRIER


@admin.register(Order)
class OrderModelAdmin(CustomModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'address', 'stream', 'change_button', 'delete_button'
    list_filter = 'id', 'phone'
    search_fields = 'product', 'id', 'owner', 'operator', 'stream'


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
class SiteSettingsAdmin(CustomShopModelAdmin):
    list_display = 'fee_for_operator', 'fee_for_currier', 'tashkent_city', 'tashkent_region', 'change_button', 'delete_button'


@admin.register(Concurs)
class ConcursAdmin(CustomShopModelAdmin):
    list_display = 'start_date', 'end_date', 'is_active', 'photo_', 'change_button', 'delete_button'

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
class TransactionModelAdmin(CustomShopModelAdmin):
    list_display = 'status', 'amount', 'message', 'bill_photo', 'owner', 'change_button', 'delete_button'
    search_fields = 'status','amount', 'message', 'owner'

    @admin.display(description='Photo')
    def bill_photo(self, obj: Transaction):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None image'


admin.site.unregister(Group)
