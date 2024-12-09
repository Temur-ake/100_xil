from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, CreateView, FormView, GenericViewError

from apps.forms import StreamModelForm, \
    OrderUpdateModelFormView, OrderModelForm, CurrierOrderForm
from apps.models import User, Category, Product, Region, Order, Stream, SiteSettings, District, Concurs
from apps.views import CustomListView, CustomCreateView, CustomUpdateView


class MyOrdersTemplateView(LoginRequiredMixin, ListView):
    template_name = 'apps/orders/my_orders.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset().filter(phone=self.request.user).order_by('-created_at')
        return qs


class OrderDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'apps/orders/order_success.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(**model_to_dict(SiteSettings.objects.first(), ('tashkent_city', 'tashkent_region', 'other_regions')))
        return ctx


class MarketListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/market/market.html'
    context_object_name = 'products'
    paginate_by = 21

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('cat')
        top = self.request.GET.get('top')
        search = self.request.GET.get('search')
        if category:
            qs = qs.filter(category__slug=category)
        if top == 'top':
            qs = qs[:3]
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs


class StreamCreateView(CreateView):
    queryset = Stream.objects.all()
    template_name = 'apps/market/market.html'
    # fields = 'name', 'discount', 'product', 'owner'
    form_class = StreamModelForm
    success_url = reverse_lazy('stream')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        text = """
            Chegirma miqdori oshib ketdi !
        """
        messages.add_message(self.request, messages.WARNING, text)
        return redirect('market')


class MyStreamsListView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/streams/my_streams.html'


class StatisticsListView(LoginRequiredMixin, ListView):
    queryset = Stream.objects.all()
    template_name = 'apps/streams/statistics.html'
    context_object_name = 'streams'

    def get_period_filter(self, qs, _type):
        today = timezone.now().date()
        monday = today - timezone.timedelta(days=today.weekday())
        first_day_of_month = today.replace(day=1)
        if _type in ('weekly', 'monthly'):
            d = {
                'weekly': [monday, today],
                'monthly': [first_day_of_month, today]
            }
            qs = qs.filter(orders__created_at__date__gte=d[_type][0], orders__created_at__date__lte=d[_type][1])
        if _type == 'today':
            qs = qs.filter(orders__created_at__date=timezone.now().date())
        if _type == 'last_day':
            qs = qs.filter(orders__created_at__date=(timezone.now() - timedelta(days=1)).date())
        return qs

    def get_queryset(self):
        qs = super().get_queryset().filter(owner=self.request.user)
        period = self.request.GET.get('period')
        qs = self.get_period_filter(qs, period)
        qs = qs.annotate(
            count_new=Count('orders', filter=Q(orders__status=Order.Status.NEW)),
            count_archived=Count('orders', filter=Q(orders__status=Order.Status.ARCHIVED)),
            count_ready_to_deliver=Count('orders', filter=Q(orders__status=Order.Status.READY_TO_DELIVER)),
            count_delivering=Count('orders', filter=Q(orders__status=Order.Status.DELIVERING)),
            count_delivered=Count('orders', filter=Q(orders__status=Order.Status.DELIVERED)),
            count_defective_product=Count('orders', filter=Q(orders__status=Order.Status.BROKEN)),
            count_returned=Count('orders', filter=Q(orders__status=Order.Status.RETURNED)),
            count_canceled=Count('orders', filter=Q(orders__status=Order.Status.CANCELED)),
            count_waiting=Count('orders', filter=Q(orders__status=Order.Status.WAITING)),
        )

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['order_types'] = Order.Status.labels
        qs = self.get_queryset()
        ctx.update(qs.aggregate(
            all_count_visits=Sum('visit_count'),
            all_count_new=Sum('count_new'),
            all_count_archived=Sum('count_archived'),
            all_count_ready_to_deliver=Sum('count_ready_to_deliver'),
            all_count_delivering=Sum('count_delivering'),
            all_count_delivered=Sum('count_delivered'),
            all_count_defective_product=Sum('count_defective_product'),
            all_count_returned=Sum('count_returned'),
            all_count_canceled=Sum('count_canceled'),
            all_count_waiting=Sum('count_waiting')
        ))
        return ctx


class CompetitionListView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/parts/concurs.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['concurs'] = Concurs.objects.filter(is_active=True).first()
        return ctx

    def get_queryset(self):
        competition = Concurs.objects.filter(is_active=True).first()
        qs = super().get_queryset()
        if competition:
            start_date = competition.start_date
            end_date = competition.end_date
            qs = super().get_queryset()
            qs = qs.exclude(type=User.Type.ADMIN).annotate(
                order_product_count=Sum('stream__orders__quantity',
                                        filter=Q(stream__orders__status=Order.Status.DELIVERED) &
                                               Q(stream__orders__created_at__gte=start_date) &
                                               Q(stream__orders__created_at__lte=end_date)
                                        )
            ).filter(order_product_count__isnull=False).order_by('-order_product_count')
        return qs


class RequestListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/parts/requests.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset().filter(stream__owner=self.request.user)
        return qs


class DiagramTemplateView(TemplateView):
    template_name = 'apps/parts/diagrams.html'


class AdminPageTemplateView(TemplateView):
    template_name = 'apps/users/admin_page.html'


class OrderListView(LoginRequiredMixin, CustomListView):
    queryset = Order.objects.select_related('product', 'stream').order_by('created_at')
    template_name = 'apps/users/operator.html'
    context_object_name = 'orders'
    paginate_by = 30

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        status = self.kwargs.get('status', 'new')
        if status != 'all':
            ctx['products'] = Product.objects.filter(orders__status=status)
        else:
            ctx['products'] = Product.objects.all()
        ctx['regions'] = Region.objects.all()
        ctx['districts'] = District.objects.all()
        ctx['all_products'] = Product.objects.all()

        return ctx

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.kwargs.get('status', 'new')
        product = self.request.GET.getlist('product')
        name = self.request.GET.get('name')
        region = self.request.GET.getlist('region')
        district = self.request.GET.get('district')
        if status:
            if status != 'all':
                qs = qs.filter(Q(status=status))
            if name:
                qs = qs.filter(Q(product__name__icontains=name))
            if region:
                qs = qs.filter(Q(region_id__in=map(int, self.request.GET.getlist('region'))))
            if district:
                qs = qs.filter(Q(district_id__in=map(int, self.request.GET.getlist('district'))))
            if product:
                qs = qs.filter(Q(product_id__in=map(int, self.request.GET.getlist('product'))))
        return qs


class OperatorOrderDetail(LoginRequiredMixin, CustomUpdateView):
    queryset = Order.objects.all()
    form_class = OrderUpdateModelFormView
    template_name = 'apps/orders/operator_change_condition.html'
    context_object_name = 'order'
    success_url = reverse_lazy('operator')

    def form_valid(self, form):
        return redirect('operator')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()
        return ctx

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        session_operator = self.request.user
        if not obj.operator:
            obj.operator = session_operator
            obj.save()
        return obj


class AddOrderCreateView(CustomCreateView):
    form_class = OrderModelForm
    template_name = 'apps/users/operator.html'
    success_url = reverse_lazy('operator')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()
        ctx['all_products'] = Product.objects.all()
        return ctx

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CurrierListView(LoginRequiredMixin, ListView, FormView):
    queryset = User.objects.all()
    form_class = CurrierOrderForm
    template_name = 'apps/currier_pages/currier_list.html'
    context_object_name = 'curriers'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=User.Type.CURRIER)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.GET.get('orders'):
            order_idies = self.request.GET.getlist('orders')
            ctx['orders'] = Order.objects.filter(id__in=order_idies).values_list('id', flat=True)
        return ctx


# class CurrierDetail(LoginRequiredMixin, DetailView, FormView):
#     queryset = User.objects.all()
#     template_name = 'apps/currier_pages/currier_briktirish.html'
#     context_object_name = 'currier'
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(type=User.Type.CURRIER)
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         qs = self.get_queryset()
#         if self.request.POST:
#             pass
#         if self.request.GET.get('currier'):
#             currier_id = int(self.request.GET.get('currier'))
#             order_idies = list(map(int, self.request.GET.get('orders').split(',')))
#             ctx['orders'] = Order.objects.filter(id__in=order_idies)
#             ctx['currier'] = qs.filter(pk=currier_id).values()[0]['phone']
#             ctx['orders'].update(currier_id=currier_id, status=Order.Status.DELIVERING)
#         return ctx

class CurrierDetail(LoginRequiredMixin, DetailView, FormView):
    queryset = User.objects.all()
    form_class = CurrierOrderForm
    template_name = 'apps/currier_pages/currier_briktirish.html'
    context_object_name = 'currier'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(type=User.Type.CURRIER)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        qs = self.get_queryset()
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            currier_id = int(self.request.POST.get('currier'))
            self.order_idies = list(map(int, self.request.POST.get('orders').split(',')))
            ctx['orders'] = Order.objects.filter(id__in=self.order_idies)
            ctx['currier_phone'] = qs.filter(pk=currier_id).values()[0]['phone']
            ctx['currier_id'] = currier_id
        return ctx

    def form_valid(self, form):
        return redirect(reverse_lazy('operator'))

    def form_invalid(self, form):
        return super().form_invalid(form)
