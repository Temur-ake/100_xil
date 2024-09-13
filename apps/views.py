from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, UpdateView, DetailView, CreateView, FormView

from apps.forms import PasswordChangeModelForm, OrderModelForm, LoginRegisterModelForm
from apps.models import User, Category, Product, Region, Order, Stream


class AllProductListView(ListView):
    queryset = Product.objects.order_by('-created_at')
    template_name = 'apps/index.html'
    context_object_name = 'products'
    paginate_by = 5

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


class StreamDetailView(DetailView):
    queryset = Stream.objects.all()
    template_name = 'apps/streams/stream_detail.html'
    context_object_name = 'stream'


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


class ProductStatistic(ListView):
    queryset = Stream.objects.all()
    template_name = 'apps/product/product_statistic.html'

    def get_queryset(self):
        return super().get_queryset().filter(product_id=self.request.GET.get('product'))


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
    fields = 'name', 'discount', 'product', 'owner'
    success_url = reverse_lazy('stream')


class MyStreamsListView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/streams/my_streams.html'


class StatisticsListView(TemplateView):
    template_name = 'apps/streams/statistics.html'


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


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')
