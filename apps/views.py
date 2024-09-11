from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, UpdateView, DetailView, CreateView

from apps.forms import PasswordChangeModelForm
from apps.models import User, Category, Product, Region, Order


class AllProductListView(ListView):
    queryset = Product.objects.all()
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
    model = User
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


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_detail.html'
    context_object_name = 'product'


class ProductSearchListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            return qs.filter(name__icontains=search)
        return qs


class ProductOrderCreateView(CreateView):
    queryset = Order.objects.all()
    fields = 'full_name', 'phone', "product", 'owner'
    template_name = 'apps/product/product_detail.html'
    success_url = reverse_lazy('success-product')
    context_object_name = 'order'


class OrderAttemptedTemplateView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'apps/orders/order_attempt.html'
    context_object_name = 'order'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner_id=self.request.user.pk).order_by('-created_at').first()


class MyOrdersListView(ListView):
    queryset = Order.objects.order_by('-created_at')
    template_name = 'apps/orders/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(owner_id=self.request.user)


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
        search = self.request.GET.get('search')
        if category:
            qs = qs.filter(category__slug=category)
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs


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


class LoginRegisterView(View):
    def get(self, request):
        return render(request, 'apps/auth/login-register.html')

    def post(self, request):
        phone = ''.join([i for i in request.POST.get('phone') if i.isdigit()])
        password = request.POST.get('password')
        user = User.objects.filter(phone=phone).first()
        if user:
            user = authenticate(request, phone=phone, password=password)
            if user:
                login(request, user)
                return redirect('main-page')
            redirect('login-page')
        new_user = User.objects.create_user(phone=phone, password=password)
        login(request, new_user)
        return redirect('main-page')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')
