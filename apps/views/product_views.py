from django.contrib import messages
from django.db.models import Sum, Q, F
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from apps.forms import OrderModelForm
from apps.models import Category, Product, Stream, User, Order


class AllProductListView(ListView):
    queryset = Product.objects.select_related('category').order_by('-created_at')
    template_name = 'apps/index.html'
    context_object_name = 'products'
    paginate_by = 80

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        # Stream.objects.filter(owner=self.request.user, stream__orders__status=Order.Status.DELIVERING).annotate(
        #     price_=F('orders__product__product_fee') - F('discount')
        # ).aggregate(all_amount=Sum('price_'))

        ctx['coins'] = (User.objects.filter(id=self.request.user.pk).annotate(
            price_=F('stream__orders__product__product_fee') - F('stream__discount')).aggregate(
            all_amount=Sum('price_', filter=Q(stream__orders__status=Order.Status.DELIVERING))))
        return ctx


class ProductListView(ListView):
    queryset = Product.objects.all().order_by('-created_at')
    template_name = 'apps/product/product_list.html'
    context_object_name = 'products'
    paginate_by = 80

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('cat')
        search = self.request.GET.get('search')
        if category:
            return qs.filter(category__slug=category)
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductStreamDetail(DetailView, FormView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_detail.html'
    form_class = OrderModelForm
    success_url = reverse_lazy('order-detail')
    context_object_name = 'product'

    def get_object(self, queryset=None):
        self._stream_discount = 0
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            stream = get_object_or_404(Stream, pk=pk)
            stream.visit_count += 1
            self._stream_discount = -stream.discount
            stream.save()
            return stream.product
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['discount'] = self._stream_discount
        ctx['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
        ctx['range_1_to_9'] = range(1, 10)
        return ctx

    def form_valid(self, form):
        order = form.save()
        return redirect('order-detail', pk=order.id)

    def form_invalid(self, form):
        message = "Noto'g'ri telefon nomer !"
        messages.add_message(self.request, messages.WARNING, message)
        product_slug = form.cleaned_data.get('product').slug
        return redirect('product-detail', slug=product_slug)


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


class ProductStatisticListView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product_statistic.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        session_product = Stream.objects.filter(product_id=self.kwargs.get('pk'), owner=self.request.user)
        ctx['my_stream_count'] = session_product.count()
        return ctx
