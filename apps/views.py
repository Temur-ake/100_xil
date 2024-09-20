import re
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Count, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView, UpdateView, DetailView, CreateView, FormView

from apps.forms import PasswordChangeModelForm, OrderModelForm, LoginRegisterModelForm, StreamModelForm
from apps.models import User, Category, Product, Region, Order, Stream


class AllProductListView(ListView):
    queryset = Product.objects.select_related('category').order_by('-created_at')
    template_name = 'apps/index.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('cat')
        if category:
            return qs.filter(category__slug=category)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/users/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    fields = 'first_name', 'last_name', 'address', 'telegram_id', 'about'
    template_name = 'apps/users/profile_settings.html'
    success_url = reverse_lazy('main-page')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()
        return ctx

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        text = """
            This telegram ID already exists please check!
                            """
        messages.add_message(self.request, messages.WARNING, text)
        return super().form_invalid(form)


class ProductDetailView(DetailView, FormView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_detail.html'
    form_class = OrderModelForm
    context_object_name = 'product'
    success_url = reverse_lazy('order-detail')

    def form_valid(self, form):
        order = form.save()
        return redirect('order-detail', pk=order.id)

    def form_invalid(self, form):
        message = """
        Invalid phone number!
        """
        messages.add_message(self.request, messages.WARNING, message)
        product_slug = form.cleaned_data.get('product').slug
        return redirect('product-detail', slug=product_slug)


class StreamDetailView(DetailView):
    queryset = Stream.objects.all()
    template_name = 'apps/streams/stream_detail.html'
    context_object_name = 'stream'

    def get_queryset(self):
        qs = super().get_queryset().filter(id=self.kwargs['pk'])
        qs.update(visit_count=F('visit_count') + 1)
        return qs


class ProductSearchListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/search_results.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            return qs.filter(name__icontains=search)
        return qs


class MyOrdersTemplateView(TemplateView):
    template_name = 'apps/orders/my_orders.html'


class OrderDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'apps/orders/order_success.html'
    context_object_name = 'order'


class MarketListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/market/market.html'
    context_object_name = 'products'
    paginate_by = 3

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
            qs = qs.order_by('-created_at')[:3]
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
            The discount amount has increased!
        """
        messages.add_message(self.request, messages.WARNING, text)
        return redirect('market')


class ProductStatisticListView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_statistic.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        session_product = Stream.objects.filter(product_id=self.kwargs.get('pk'),
                                                owner_id=self.request.user.pk)
        ctx['my_stream_count'] = session_product.count()
        return ctx


# User.objects.annotate(balance__gte=F('summa'))

class MyStreamsListView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/streams/my_streams.html'


class StatisticsListView(ListView):
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


class PasswordUpdateView(UpdateView):
    template_name = 'apps/users/profile_settings.html'
    form_class = PasswordChangeModelForm
    success_url = reverse_lazy('main-page')

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        return redirect('pass-settings')

    def get_success_url(self):
        login(self.request, self.request.user)
        return super().get_success_url()


class LoginRegisterView(FormView):
    template_name = 'apps/auth/login-register.html'
    form_class = LoginRegisterModelForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('main-page')

    def form_invalid(self, form):
        phone = re.sub(r'[^\d]', '', form.data['phone'])
        password = form.data['password']
        text = ""
        user = authenticate(self.request, phone=phone, password=password)
        if len(phone) != 12 or not phone.startswith('998') or user is None:
            text = "Incorrect password or phone number!"
        if not phone or not password:
            text = "Phone and password cannot be blank"
        if text:
            messages.add_message(self.request, messages.WARNING, text)
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')
