import datetime
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# from django.db.models import DateTimeField
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm
from apps.views.auth_views import SuccessValijonTemplateView

admin.site.login_form = CustomAdminAuthenticationForm

from apps.models import Category, SiteSettings, OperatorUserProxy, Product, User, Concurs, \
    Operator, Transaction, OperatorStatisticUserProxy, District
from apps.models.proxy import CustomerUserProxy, CurrierUserProxy, NewOrderProxy, \
    DeliveringOrderProxy, DeliveredOrderProxy, ManagerUserProxy, FreshfoodKuryerlari, FreshCurrierStatisticUserProxy


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
        'Transaction': 'label3',
        'CurrierStatisticUserProxy': 'label',
        'FreshfoodKuryerlari': 'label',
        'Fresh_food_Statistikasi': 'label',
        'FreshCurrierStatisticUserProxy': 'label2'
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
        (_("Personal info"),
         {"fields": ("first_name", "last_name", 'region', 'district', 'type', 'balance', 'brand')}),
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

    # Display photo in the list display
    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')

    # Other display fields for the user list
    ordering = ['phone']
    list_display = ['id', 'phone', 'first_name', 'last_name', 'image', 'type', 'brand', 'change_button',
                    'delete_button']

    # The other admin settings...
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "photo", "type", "balance", "brand")}),
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

    # Media for custom JS (if necessary)
    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/custom.js'  # Path to your custom JS
        )


# @admin.register(AdminUserProxy)
# class AdminUserProxyModelAdmin(CustomUserAdmin):
#     list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'change_button', 'delete_button'
#     _type = User.Type.ADMIN
#
#     @admin.display(description=_('Photo'))
#     def image(self, obj):
#         img = obj.photo
#         if img:
#             return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
#         return _('No Image')


@admin.register(ManagerUserProxy)
class ManagerUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'change_button', 'delete_button'
    _type = User.Type.MANAGER

    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')


class OperatorStackedInline(StackedInline):
    model = Operator


@admin.register(OperatorUserProxy)
class OperatorUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'readies', 'change_button', 'delete_button'
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

    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')


@admin.register(OperatorStatisticUserProxy)
class OperatorStatisticUserProxyModelAdmin(CustomUserAdmin):
    change_list_template = 'admin/operator_statistics.html'
    _type = User.Type.OPERATOR

    def changelist_view(self, request, extra_context=None):
        # Call the parent class's changelist view
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # Define the metrics
        metrics = {
            'total': Count('operator_orders'),
            'succeed': Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED)),
            'operator_full_name': F('first_name')
        }

        # Annotate the queryset with metrics
        response.context_data['summary'] = list(
            qs
            .annotate(**metrics)
            .annotate(
                # Safe division to avoid ZeroDivisionError
                of_total_talks=Case(
                    When(total=0, then=Value(0)),  # If total is zero, return 0
                    default=F('succeed') * 100 / F('total'),  # Otherwise, divide as usual
                    output_field=IntegerField()
                )
            )
            .order_by('first_name')
        )

        # Prepare the total summary for the metrics
        updated_metrics = metrics.copy()  # Copy the dictionary to update it
        del updated_metrics['operator_full_name']  # Remove the 'operator_full_name' key
        response.context_data['summary_total'] = dict(
            qs.aggregate(**updated_metrics)
        )

        # Calculate the overall percentage
        total_succeed = response.context_data['summary_total'].get('succeed', 0)
        total_count = max(response.context_data['summary_total'].get('total', 1), 1)  # Prevent division by zero
        response.context_data['overall'] = (total_succeed * 100) // total_count

        # Calculate the statistics over time (monthly)
        summary_over_time = OperatorStatisticUserProxy.objects.filter(
            operator_orders__status=Order.Status.DELIVERED
        ).annotate(
            period=TruncMonth('operator_orders__created_at', output_field=DateTimeField())
        ).values('period').annotate(
            total=Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED))
        ).order_by('period')

        # Get the range (low/high) of totals for the entire time range
        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        # Prepare the summary over time with percentages
        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low) / (high - low) * 100 if high > low else 0,
        } for x in summary_over_time]

        return response


from django.db.models import Case, When, Value, IntegerField, Min, Max, Q, F
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, datetime, TruncDate
from django.contrib import admin
from .models import Order
from .models.proxy import CurrierStatisticUserProxy  # Assuming this is your proxy model
from django.utils import timezone


@admin.register(CurrierStatisticUserProxy)
class CurrierStatisticUserProxyModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/currier_statistics.html'
    _type = User.Type.CURRIER

    def changelist_view(self, request, extra_context=None):
        # Call the parent class's changelist view
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # Define the metrics for courier statistics
        metrics = {
            'total': Count('currier_orders'),  # Count all orders assigned to the courier
            'delivered': Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED)),
            # Count delivered orders
            'currier_full_name': F('first_name')  # Adjust for courier's name
        }

        # Annotate the queryset with the defined metrics
        response.context_data['summary'] = list(
            qs
            .annotate(**metrics)
            .annotate(
                # Safe division to avoid ZeroDivisionError
                of_total_deliveries=Case(
                    When(total=0, then=Value(0)),
                    default=F('delivered') * 100 / F('total'),  # Otherwise, divide delivered by total
                    output_field=IntegerField()
                )
            )
            .order_by('first_name')  # Adjust ordering if necessary
        )

        # Prepare the total summary for the metrics (courier-wide summary)
        updated_metrics = metrics.copy()  # Copy the dictionary to update it
        del updated_metrics['currier_full_name']  # Remove the name key
        response.context_data['summary_total'] = dict(
            qs.aggregate(**updated_metrics)
        )

        # Calculate the overall percentage for all couriers
        total_delivered = response.context_data['summary_total'].get('delivered', 0)
        total_count = max(response.context_data['summary_total'].get('total', 1), 1)  # Prevent division by zero
        response.context_data['overall'] = (total_delivered * 100) // total_count

        # Calculate statistics over time (monthly, weekly, and daily)
        summary_over_time = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED
        )

        # Monthly statistics for courier orders
        summary_over_time_monthly = summary_over_time.annotate(
            period_month=TruncMonth('currier_orders__created_at')
        ).values('period_month').annotate(
            total=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        ).order_by('period_month')

        # Weekly statistics for courier orders
        summary_over_time_weekly = summary_over_time.annotate(
            period_week=TruncWeek('currier_orders__created_at')
        ).values('period_week').annotate(
            total=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        ).order_by('period_week')

        # Daily statistics for courier orders
        summary_over_time_daily = summary_over_time.annotate(
            period_day=TruncDay('currier_orders__created_at')
        ).values('period_day').annotate(
            total=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        ).order_by('period_day')

        # Get the range (low/high) of totals for the entire time range
        summary_range_monthly = summary_over_time_monthly.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high_month = summary_range_monthly.get('high', 0)
        low_month = summary_range_monthly.get('low', 0)

        summary_range_weekly = summary_over_time_weekly.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high_week = summary_range_weekly.get('high', 0)
        low_week = summary_range_weekly.get('low', 0)

        summary_range_daily = summary_over_time_daily.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high_day = summary_range_daily.get('high', 0)
        low_day = summary_range_daily.get('low', 0)

        # Prepare the summary over time with percentages (monthly)
        response.context_data['summary_over_time_monthly'] = [{
            'period': x['period_month'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low_month) / (high_month - low_month) * 100 if high_month > low_month else 0,
        } for x in summary_over_time_monthly]

        # Prepare the summary over time with percentages (weekly)
        response.context_data['summary_over_time_weekly'] = [{
            'period': x['period_week'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low_week) / (high_week - low_week) * 100 if high_week > low_week else 0,
        } for x in summary_over_time_weekly]

        # Prepare the summary over time with percentages (daily)
        response.context_data['summary_over_time_daily'] = [{
            'period': x['period_day'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low_day) / (high_day - low_day) * 100 if high_day > low_day else 0,
        } for x in summary_over_time_daily]

        today = timezone.now().date()

        # Today's statistics (delivered orders today)
        todays_stats = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__created_at__date=today
        ).aggregate(
            delivered_today=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        )
        response.context_data['todays_stats'] = todays_stats['delivered_today']

        # Weekly statistics (delivered orders this week)
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)

        weekly_stats = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__created_at__range=[start_of_week, end_of_week]
        ).aggregate(
            delivered_this_week=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        )
        response.context_data['weekly_stats'] = weekly_stats['delivered_this_week']

        # Monthly statistics (delivered orders this month)
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=1) + timezone.timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timezone.timedelta(days=1)

        monthly_stats = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__created_at__range=[start_of_month, end_of_month]
        ).aggregate(
            delivered_this_month=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        )
        response.context_data['monthly_stats'] = monthly_stats['delivered_this_month']

        return response


@admin.register(District)
class DistrictModelAdmin(ModelAdmin):
    search_fields = 'name',


@admin.register(CustomerUserProxy)
class CustomerUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'change_button', 'delete_button'
    _type = User.Type.CUSTOMER

    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')


@admin.register(CurrierUserProxy)
class CurrierUserProxyModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'brand', 'change_button', 'delete_button'
    _type = User.Type.CURRIER

    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')


@admin.register(Order)
class OrderModelAdmin(CustomModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'manzil', 'stream', 'change_button', 'delete_button'
    list_filter = 'id', 'phone'
    search_fields = 'product', 'id', 'owner', 'operator', 'stream'


@admin.register(NewOrderProxy)
class NewOrderProxyModelAdmin(OrderModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'manzil', 'stream', 'change_button', 'delete_button'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.NEW, product__owner=request.user.brand)


@admin.register(FreshfoodKuryerlari)
class FreshfoodKuryerlariModelAdmin(OrderModelAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'brand', 'change_button', 'delete_button'
    _type = User.Type.CURRIER

    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')

    def get_queryset(self, request):
        # Assuming 'brand' is a ForeignKey to the `User` model
        brand_user = User.objects.get(phone='979631626')
        return super().get_queryset(request).filter(brand=brand_user)


from django.db.models import Count, Case, When, Value, IntegerField, Q, F
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.contrib import admin
from .models import Order
from .models.proxy import CurrierStatisticUserProxy  # Assuming this is your proxy model
from django.utils import timezone


@admin.register(FreshCurrierStatisticUserProxy)
class CurrierStatisticUserProxyModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/currier_statistics.html'
    _type = User.Type.CURRIER  # Ensure this is for couriers

    def changelist_view(self, request, extra_context=None):

        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        brand_user = User.objects.get(phone='979631626')
        qs = qs.filter(brand=brand_user)

        metrics = {
            'total': Count('currier_orders'),
            'delivered': Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED)),

            'currier_full_name': F('first_name')
        }

        response.context_data['summary'] = list(
            qs
            .annotate(**metrics)
            .annotate(

                of_total_deliveries=Case(
                    When(total=0, then=Value(0)),
                    default=F('delivered') * 100 / F('total'),
                    output_field=IntegerField()
                )
            )
            .order_by('first_name')
        )

        updated_metrics = metrics.copy()
        del updated_metrics['currier_full_name']
        response.context_data['summary_total'] = dict(
            qs.aggregate(**updated_metrics)
        )

        # Calculate the overall percentage for all couriers
        total_delivered = response.context_data['summary_total'].get('delivered', 0)
        total_count = max(response.context_data['summary_total'].get('total', 1), 1)  # Prevent division by zero
        response.context_data['overall'] = (total_delivered * 100) // total_count

        brand_user = User.objects.get(phone='979631626')

        summary_over_time = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            brand=brand_user
        )

        # Monthly statistics for courier orders
        summary_over_time_monthly = summary_over_time.annotate(
            period_month=TruncMonth('currier_orders__created_at')
        ).values('period_month').annotate(
            total=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED, brand=brand_user))
        ).order_by('period_month')

        # Weekly statistics for courier orders
        summary_over_time_weekly = summary_over_time.annotate(
            period_week=TruncWeek('currier_orders__created_at')
        ).values('period_week').annotate(
            total=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED, brand=brand_user))
        ).order_by('period_week')

        # Daily statistics for courier orders
        summary_over_time_daily = summary_over_time.annotate(
            period_day=TruncDay('currier_orders__created_at')
        ).values('period_day').annotate(
            total=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED, brand=brand_user))
        ).order_by('period_day')

        # Get the range (low/high) of totals for the entire time range
        summary_range_monthly = summary_over_time_monthly.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high_month = summary_range_monthly.get('high', 0)
        low_month = summary_range_monthly.get('low', 0)

        summary_range_weekly = summary_over_time_weekly.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high_week = summary_range_weekly.get('high', 0)
        low_week = summary_range_weekly.get('low', 0)

        summary_range_daily = summary_over_time_daily.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high_day = summary_range_daily.get('high', 0)
        low_day = summary_range_daily.get('low', 0)

        # Prepare the summary over time with percentages (monthly)
        response.context_data['summary_over_time_monthly'] = [{
            'period': x['period_month'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low_month) / (high_month - low_month) * 100 if high_month > low_month else 0,
        } for x in summary_over_time_monthly]

        # Prepare the summary over time with percentages (weekly)
        response.context_data['summary_over_time_weekly'] = [{
            'period': x['period_week'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low_week) / (high_week - low_week) * 100 if high_week > low_week else 0,
        } for x in summary_over_time_weekly]

        # Prepare the summary over time with percentages (daily)
        response.context_data['summary_over_time_daily'] = [{
            'period': x['period_day'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low_day) / (high_day - low_day) * 100 if high_day > low_day else 0,
        } for x in summary_over_time_daily]

        today = timezone.now().date()

        todays_stats = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__created_at__date=today,
            brand=brand_user
        ).aggregate(
            delivered_today=Count('currier_orders',
                                  filter=Q(currier_orders__status=Order.Status.DELIVERED, brand=brand_user))
        )
        response.context_data['todays_stats'] = todays_stats['delivered_today']

        # Weekly statistics (delivered orders this week)
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)

        weekly_stats = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__created_at__range=[start_of_week, end_of_week],
            brand=brand_user  # Filter couriers by brand
        ).aggregate(
            delivered_this_week=Count('currier_orders',
                                      filter=Q(currier_orders__status=Order.Status.DELIVERED, brand=brand_user))
        )
        response.context_data['weekly_stats'] = weekly_stats['delivered_this_week']

        # Monthly statistics (delivered orders this month)
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=1) + timezone.timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timezone.timedelta(days=1)

        monthly_stats = CurrierStatisticUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__created_at__range=[start_of_month, end_of_month],
            brand=brand_user  # Filter couriers by brand
        ).aggregate(
            delivered_this_month=Count('currier_orders',
                                       filter=Q(currier_orders__status=Order.Status.DELIVERED, brand=brand_user))
        )
        response.context_data['monthly_stats'] = monthly_stats['delivered_this_month']

        return response


from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils.translation import gettext_lazy as _
from .models.proxy import FreshStatisticProxy, Order, User
import datetime


@admin.register(FreshStatisticProxy)
class FreshStatisticOrderModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/fresh_statistics.html'
    list_display = ['product__owner', 'delivered_count', 'delivering_count', 'new_count', 'total_count']

    def get_queryset(self, request):
        product_owner = User.objects.filter(phone='979631626').first()
        if product_owner:
            return FreshStatisticProxy.objects.filter(product__owner=product_owner).distinct()
        return FreshStatisticProxy.objects.none()

    def get_summary_over_time(self, product_owner):
        time_periods = ['daily', 'weekly', 'monthly']
        summary_over_time = []

        total_orders = Order.objects.filter(product__owner=product_owner).count()

        today = datetime.date.today()

        for period in time_periods:
            data = Order.objects.filter(product__owner=product_owner)

            if period == 'daily':
                data = data.annotate(date_only=TruncDate('created_at')).filter(date_only=today)
            elif period == 'weekly':
                data = data.annotate(week_start=TruncWeek('created_at')).filter(week_start__lte=today)
            elif period == 'monthly':
                data = data.annotate(month_start=TruncMonth('created_at')).filter(month_start__lte=today)

            delivered_count = data.filter(
                status='delivered').count()
            delivering_count = data.filter(status='delivering').count()
            new_count = data.filter(status='new').count()

            pct = (delivered_count / total_orders) * 100 if total_orders > 0 else 0

            summary_over_time.append({
                'period': period,
                'delivered_count': delivered_count,
                'delivering_count': delivering_count,
                'new_count': new_count,
                'total_count': total_orders,
                'pct': pct,
            })

        return summary_over_time

    @admin.display(description='Delivered Orders')
    def delivered_count(self, obj):
        return obj.delivered_count

    @admin.display(description='Delivering Orders')
    def delivering_count(self, obj):
        return obj.delivering_count

    @admin.display(description='New Orders')
    def new_count(self, obj):
        return obj.new_count

    @admin.display(description='Total Orders')
    def total_count(self, obj):
        return obj.total_count

    def changelist_view(self, request, extra_context=None):

        product_owner = User.objects.filter(phone='979631626').first()

        if product_owner:
            todays_stats = self.get_summary_over_time(product_owner)
            weekly_stats = self.get_summary_over_time(product_owner)
            monthly_stats = self.get_summary_over_time(product_owner)

            extra_context = extra_context or {}
            extra_context.update({
                'todays_stats': todays_stats,
                'weekly_stats': weekly_stats,
                'monthly_stats': monthly_stats,
                'summary': self.get_summary_over_time(product_owner),
                'summary_total': self.get_summary_over_time(product_owner),
                'summary_over_time': self.get_summary_over_time(product_owner),
            })

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(DeliveringOrderProxy)
class DeliveringOrderProxyModelAdmin(OrderModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'manzil', 'stream', 'change_button', 'delete_button'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.DELIVERING, product__owner=request.user.brand)


@admin.register(DeliveredOrderProxy)
class DeliveredOrderProxyModelAdmin(OrderModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'manzil', 'stream', 'change_button', 'delete_button'

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status=Order.Status.DELIVERED, product__owner=request.user.brand)


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
    search_fields = 'status', 'amount', 'message', 'owner'

    @admin.display(description='Photo')
    def bill_photo(self, obj: Transaction):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None image'


# @admin.register(Fresh_food_Kuryerlari)
# class Fresh_food_KuryerlariModelAdmin(CustomUserAdmin):
#     # list_display = ('phone', 'first_name', 'last_name', 'image', 'type', 'brand', 'change_button', 'delete_button')
#
#
#     def get_queryset(self, request):
#         # Filtering Fresh_food_Kuryerlari by the owner's phone number
#         product_owner = User.objects.filter(phone='979631626').first()
#         if product_owner:
#             # Assuming Fresh_food_Kuryerlari is related to Product, and Product has an owner
#             return super().get_queryset(request).filter(product__owner=product_owner)
#         return super().get_queryset(request)


admin.site.unregister(Group)

# @admin.register(BrokenOrderProxy)
# class BrokenOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.BROKEN, product__owner=request.user.brand)


# @admin.register(ReturnedOrderProxy)
# class ReturnedOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.RETURNED, product__owner=request.user.brand)


# @admin.register(CanceledOrderProxy)
# class CanceledOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.CANCELED, product__owner=request.user.brand)


# @admin.register(WaitingOrderProxy)
# class WaitingOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.WAITING, product__owner=request.user.brand)

# @admin.register(ArchivedOrderProxy)
# class ArchivedOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.ARCHIVED, product__owner=request.user.brand)


# @admin.register(ReadyToDeliverOrderProxy)
# class ReadyToDeliverOrderProxyModelAdmin(OrderModelAdmin):
#
#     def get_queryset(self, request):
#         return super().get_queryset(request).filter(status=Order.Status.READY_TO_DELIVER,
#                                                     product__owner=request.user.brand)
