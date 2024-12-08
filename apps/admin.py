from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# from django.db.models import DateTimeField
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.forms import CustomAdminAuthenticationForm
from apps.views.auth_views import SuccessValijonTemplateView
from .models.product import DescriptionImage

admin.site.login_form = CustomAdminAuthenticationForm

from apps.models import Category, SiteSettings, Product, User, Concurs, \
    Transaction, District
from apps.models.proxy import CustomerUserProxy, MeningKuryerlarimUserProxy, NewOrderProxy, \
    DeliveringOrderProxy, DeliveredOrderProxy, ManagerUserProxy, \
    BarchaKuryerlarUserProxy, UmumiyRaqamlarProxy
from django.contrib import admin


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
        'User': 'label',
        'ManagerUserProxy': 'label',
        'CustomerUserProxy': 'label',
        'SiteSettings': 'label3',
        'Concurs': 'label3',
        'Transaction': 'label3',
        'BarchaKuryerlarStatistikasi': 'label',
        'BarchaBizneslarStatistikalari': 'label',
        'BarchaKuryerlar': 'label',

        'Category': 'label3',
        'Product': 'label3',

        'NewOrderProxy': 'label2',
        'DeliveringOrderProxy': 'label2',
        'DeliveredOrderProxy': 'label2',

        'MeningKuryerlarim': 'label',
        'MeningKuryerlarimStatistikasi': 'label',
        'MeningBiznesimStatistikasi': 'label',
        'UmumiyRaqamlar': 'label'
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
                "fields": ('phone', "password1", "password2"),
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


class DescriptionImageInline(admin.StackedInline):
    model = DescriptionImage
    extra = 1  # Number of empty forms displayed
    verbose_name = _('Description Image')
    verbose_name_plural = _('Description Images')


@admin.register(Product)
class ProductModelAdmin(CustomShopModelAdmin):
    list_display = 'id', 'name', 'price', 'quantity', 'gfvhb', 'change_button', 'delete_button'
    search_fields = 'id', 'name', 'price'
    inlines = [DescriptionImageInline]

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
                "fields": ('phone', "password1", "password2"),
            },
        ),
    )

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/5.0.6/jquery.inputmask.min.js",
            'apps/js/custom.js'  # Path to your custom JS
        )


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


from django.contrib import admin
from .models.proxy import BarchaKuryerlarStatistikasiUserProxy


@admin.register(BarchaKuryerlarStatistikasiUserProxy)
class BarchaKuryerlarStatistikasiModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/currier_statistics.html'

    def changelist_view(self, request, extra_context=None):
        # Call the parent class's changelist view
        response = super().changelist_view(request, extra_context)

        today = timezone.now().date()

        # Metrics for each courier
        metrics = {
            'total': Count('currier_orders'),
            'delivered': Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED)),
            'currier_full_name': F('first_name')
        }

        # Annotate the courier queryset with these metrics
        response.context_data['summary'] = list(
            response.context_data['cl'].queryset.annotate(**metrics)
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
            response.context_data['cl'].queryset.aggregate(**updated_metrics)
        )

        total_delivered = response.context_data['summary_total'].get('delivered', 0)
        total_count = max(response.context_data['summary_total'].get('total', 1), 1)
        response.context_data['overall'] = (total_delivered * 100) // total_count

        todays_stats = BarchaKuryerlarStatistikasiUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__send_date__date=today
        ).aggregate(
            delivered_today=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        )
        response.context_data['todays_stats'] = todays_stats['delivered_today']

        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=28) + timezone.timedelta(days=4)
        end_of_month = end_of_month - timezone.timedelta(days=end_of_month.day)

        monthly_stats = BarchaKuryerlarStatistikasiUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__send_date__range=[start_of_month, end_of_month]
        ).aggregate(
            delivered_this_month=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        )
        response.context_data['monthly_stats'] = monthly_stats['delivered_this_month']

        return response


from django.db.models import Count, Q
from django.utils import timezone


@admin.register(UmumiyRaqamlarProxy)
class UmumiyRaqamlarModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/umumiy_raqamlar_statistics.html'  # Custom template for the changelist view

    def get_queryset(self, request):
        # Get the product owner (business owner)
        product_owner = User.objects.filter(phone=request.user.phone, type=User.Type.CUSTOMER).first()
        if product_owner:
            # Filter the UmumiyRaqamlarProxy by product owner's brand if available
            return UmumiyRaqamlarProxy.objects.filter(product__owner=product_owner,
                                                      product__owner__brand=product_owner.brand).distinct()
        return UmumiyRaqamlarProxy.objects.none()

    def changelist_view(self, request, extra_context=None):
        # Call the parent class's changelist view
        response = super().changelist_view(request, extra_context)

        # Get the product owner (business owner) based on the logged-in user
        product_owner = User.objects.filter(phone=request.user.phone, type=User.Type.CUSTOMER).first()

        # Get today's date and start of the current month
        today = timezone.now().date()  # Current date
        start_of_month = today.replace(day=1)  # Start of the current month

        # Calculate the end of the current month
        next_month = today.replace(day=28) + timezone.timedelta(days=4)  # Go to the next month
        end_of_month = next_month - timezone.timedelta(days=next_month.day)  # Get the last day of the current month

        # Filter today's deliveries (status=DELIVERED) for the current user/brand
        todays_deliveries = Order.objects.filter(
            send_date__date=today  # Only today's deliveries
        )

        if product_owner:
            todays_deliveries = todays_deliveries.filter(product__owner=product_owner,
                                                         product__owner__brand=product_owner.brand)

        todays_deliveries = todays_deliveries.aggregate(
            delivered_today=Count('id', filter=Q(status=Order.Status.DELIVERED)),
            delivering_today=Count('id', filter=Q(status=Order.Status.DELIVERING)),
            # new_today=Count('id', filter=Q(status=Order.Status.NEW)),
        )

        # Filter monthly deliveries (from 1st of the month to the end of the current month)
        monthly_deliveries = Order.objects.filter(
            status=Order.Status.DELIVERED,
            send_date__range=[start_of_month, end_of_month]  # Ensure full month is captured
        )

        if product_owner:
            monthly_deliveries = monthly_deliveries.filter(product__owner=product_owner,
                                                           product__owner__brand=product_owner.brand)

        monthly_deliveries = monthly_deliveries.aggregate(
            delivered_this_month=Count('id', filter=Q(status=Order.Status.DELIVERED)),
            delivering_this_month=Count('id', filter=Q(status=Order.Status.DELIVERING)),
            # new_this_month=Count('id', filter=Q(status=Order.Status.NEW)),
        )

        # Add the statistics to the context data
        response.context_data['todays_stats'] = todays_deliveries
        response.context_data['monthly_stats'] = monthly_deliveries

        return response


from django.contrib import admin
from .models.proxy import MeningKuryerlarimStatistikasiUserProxy, Order

from django.db.models import Count, Q, F, Case, When, Value, IntegerField
from django.utils import timezone


@admin.register(MeningKuryerlarimStatistikasiUserProxy)
class MeningKuryerlarimStatistikasiModelAdmin(admin.ModelAdmin):
    change_list_template = 'admin/currier_statistics.html'

    def changelist_view(self, request, extra_context=None):
        # Call the parent class's changelist view
        response = super().changelist_view(request, extra_context)

        # Get the user's brand from the request
        user_brand = User.objects.filter(phone=request.user.phone).first()

        if user_brand:
            # If user has a brand, filter couriers by their brand
            qs = super().get_queryset(request).filter(brand=user_brand)
        else:
            # If no brand found, fetch all couriers
            qs = super().get_queryset(request)

        today = timezone.now().date()

        # Metrics for each courier
        metrics = {
            'total': Count('currier_orders'),
            'delivered': Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED)),
            'currier_full_name': F('first_name')
        }

        # Annotate the courier queryset with these metrics
        response.context_data['summary'] = list(
            qs.annotate(**metrics)
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

        # Calculate overall statistics
        total_delivered = response.context_data['summary_total'].get('delivered', 0)
        total_count = max(response.context_data['summary_total'].get('total', 1), 1)
        response.context_data['overall'] = (total_delivered * 100) // total_count

        # Today's stats (filtered by brand)
        todays_stats = MeningKuryerlarimStatistikasiUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__send_date__date=today,
        )

        # If the user has a brand, filter the stats by brand
        if user_brand:
            todays_stats = todays_stats.filter(brand=user_brand)

        todays_stats = todays_stats.aggregate(
            delivered_today=Count('currier_orders', filter=Q(currier_orders__status=Order.Status.DELIVERED))
        )
        response.context_data['todays_stats'] = todays_stats['delivered_today']

        # Monthly stats (filtered by brand)
        start_of_month = today.replace(day=1)
        end_of_month = today.replace(day=28) + timezone.timedelta(days=4)
        end_of_month = end_of_month - timezone.timedelta(days=end_of_month.day)

        monthly_stats = MeningKuryerlarimStatistikasiUserProxy.objects.filter(
            currier_orders__status=Order.Status.DELIVERED,
            currier_orders__send_date__range=[start_of_month, end_of_month],
        )

        # If the user has a brand, filter the stats by brand
        if user_brand:
            monthly_stats = monthly_stats.filter(brand=user_brand)

        monthly_stats = monthly_stats.aggregate(
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


@admin.register(MeningKuryerlarimUserProxy)
class MeningKuryerlarimModelAdmin(CustomUserAdmin):
    list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'brand', 'change_button', 'delete_button'
    _type = User.Type.CURRIER

    @admin.display(description=_('Photo'))
    def image(self, obj):
        img = obj.photo
        if img:
            return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
        return _('No Image')

    def get_queryset(self, request):
        user_brand = User.objects.filter(phone=request.user.phone).first()

        if user_brand:
            qs = super().get_queryset(request).filter(brand=user_brand)  # Filter by the user's brand
        else:
            qs = super().get_queryset(request)  # If no brand found, fetch all couriers
        return qs


@admin.register(BarchaKuryerlarUserProxy)
class BarchaKuryerlarModelAdmin(CustomUserAdmin):
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
    list_display = 'id', 'status', 'phone', 'product', 'quantity', 'owner', 'operator', 'currier', 'manzil', 'stream', 'change_button', 'delete_button'

    def get_queryset(self, request):
        if request.user.phone == '970501655':
            return super().get_queryset(request).filter(status=Order.Status.NEW)
        elif request.user.Type.CURRIER:
            return super().get_queryset(request).filter(product__owner=request.user.brand)
        else:
            owner = User.objects.filter(phone=request.user.phone).first()
            return super().get_queryset(request).filter(status=Order.Status.NEW, product__owner=owner)


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models.proxy import Order, User, MyBiznesStatisticProxy


@admin.register(MyBiznesStatisticProxy)
class MeningBiznesimStatistikasiProxyOrderModelAdmin(CustomModelAdmin):
    list_display = 'id', 'status', 'product', 'quantity', 'phone', 'currier', 'manzil'
    list_filter = 'id', 'phone'
    search_fields = 'product', 'id', 'owner', 'operator', 'stream'

    def get_queryset(self, request):
        product_owner = User.objects.filter(phone=request.user.phone, type=User.Type.CUSTOMER).first()
        if product_owner:
            return MyBiznesStatisticProxy.objects.filter(product__owner=product_owner).distinct()
        return MyBiznesStatisticProxy.objects.none()


@admin.register(DeliveringOrderProxy)
class DeliveringOrderProxyModelAdmin(OrderModelAdmin):
    list_display = 'id', 'status', 'phone', 'product', 'quantity', 'owner', 'operator', 'currier', 'manzil', 'stream', 'change_button', 'delete_button'

    def get_queryset(self, request):
        if request.user.phone == '970501655':
            return super().get_queryset(request).filter(status=Order.Status.DELIVERING)
        else:
            owner = User.objects.filter(phone=request.user.phone).first()
            return super().get_queryset(request).filter(status=Order.Status.DELIVERING, product__owner=owner)


@admin.register(DeliveredOrderProxy)
class DeliveredOrderProxyModelAdmin(OrderModelAdmin):
    list_display = 'id', 'quantity', 'status', 'phone', 'product', 'owner', 'operator', 'currier', 'manzil', 'change_button', 'delete_button'

    def get_queryset(self, request):
        if request.user.phone == '970501655':
            return super().get_queryset(request).filter(status=Order.Status.DELIVERED)
        else:
            self.list_display = 'id', 'status', 'phone', 'product', 'quantity', 'owner', 'operator', 'currier', 'manzil'
            owner = User.objects.filter(phone=request.user.phone).first()
            return super().get_queryset(request).filter(status=Order.Status.DELIVERED, product__owner=owner)


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


admin.site.unregister(Group)

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


# operator
#
# class OperatorStackedInline(StackedInline):
#     model = Operator
#
#
# @admin.register(OperatorUserProxy)
# class OperatorUserProxyModelAdmin(CustomUserAdmin):
#     list_display = 'phone', 'first_name', 'last_name', 'image', 'type', 'readies', 'change_button', 'delete_button'
#     _type = User.Type.OPERATOR
#     inlines = OperatorStackedInline,
#
#     @admin.display(description=_('Amount of ready to delivery'))
#     def readies(self, obj: OperatorUserProxy):
#         count = Order.objects.filter(Q(status=Order.Status.READY_TO_DELIVER) & Q(operator=obj)).count()
#         if count > 0:
#             url = reverse(f'admin:{obj._meta.app_label}_{Order._meta.model_name}_changelist')
#             url += f'?status={Order.Status.READY_TO_DELIVER}&operator__id__exact={obj.id}'
#             return format_html('<a href="{}">{}</a>', url, count)
#         return count
#
#     @admin.display(description=_('Photo'))
#     def image(self, obj):
#         img = obj.photo
#         if img:
#             return mark_safe(f"<img src='{img.url}' alt='img' width='60px' height='60px'/>")
#         return _('No Image')
#
#
# @admin.register(OperatorStatisticUserProxy)
# class OperatorStatisticUserProxyModelAdmin(CustomUserAdmin):
#     change_list_template = 'admin/operator_statistics.html'
#     _type = User.Type.OPERATOR
#
#     def changelist_view(self, request, extra_context=None):
#         # Call the parent class's changelist view
#         response = super().changelist_view(request, extra_context)
#
#         try:
#             qs = response.context_data['cl'].queryset
#         except (AttributeError, KeyError):
#             return response
#
#         # Define the metrics
#         metrics = {
#             'total': Count('operator_orders'),
#             'succeed': Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED)),
#             'operator_full_name': F('first_name')
#         }
#
#         # Annotate the queryset with metrics
#         response.context_data['summary'] = list(
#             qs
#             .annotate(**metrics)
#             .annotate(
#                 # Safe division to avoid ZeroDivisionError
#                 of_total_talks=Case(
#                     When(total=0, then=Value(0)),  # If total is zero, return 0
#                     default=F('succeed') * 100 / F('total'),  # Otherwise, divide as usual
#                     output_field=IntegerField()
#                 )
#             )
#             .order_by('first_name')
#         )
#
#         # Prepare the total summary for the metrics
#         updated_metrics = metrics.copy()  # Copy the dictionary to update it
#         del updated_metrics['operator_full_name']  # Remove the 'operator_full_name' key
#         response.context_data['summary_total'] = dict(
#             qs.aggregate(**updated_metrics)
#         )
#
#         # Calculate the overall percentage
#         total_succeed = response.context_data['summary_total'].get('succeed', 0)
#         total_count = max(response.context_data['summary_total'].get('total', 1), 1)  # Prevent division by zero
#         response.context_data['overall'] = (total_succeed * 100) // total_count
#
#         # Calculate the statistics over time (monthly)
#         summary_over_time = OperatorStatisticUserProxy.objects.filter(
#             operator_orders__status=Order.Status.DELIVERED
#         ).annotate(
#             period=TruncMonth('operator_orders__created_at', output_field=DateTimeField())
#         ).values('period').annotate(
#             total=Count('operator_orders', filter=Q(operator_orders__status=Order.Status.DELIVERED))
#         ).order_by('period')
#
#         # Get the range (low/high) of totals for the entire time range
#         summary_range = summary_over_time.aggregate(
#             low=Min('total'),
#             high=Max('total'),
#         )
#         high = summary_range.get('high', 0)
#         low = summary_range.get('low', 0)
#
#         # Prepare the summary over time with percentages
#         response.context_data['summary_over_time'] = [{
#             'period': x['period'],
#             'total': x['total'] or 0,
#             'pct': ((x['total'] or 0) - low) / (high - low) * 100 if high > low else 0,
#         } for x in summary_over_time]
#
#         return response
