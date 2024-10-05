from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from apps.forms import TransactionModelForm
from apps.models import Transaction, SiteSettings


class PaymentListView(LoginRequiredMixin, ListView):
    queryset = Transaction.objects.all()
    template_name = 'apps/parts/payment.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        qs = super().get_queryset().filter(owner=self.request.user).order_by('-created_at')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['min_balance'] = SiteSettings.objects.values_list('min_balance_amount', flat=True).first()
        return ctx


class PaymentFormView(LoginRequiredMixin, FormView):
    queryset = Transaction.objects.all()
    template_name = 'apps/parts/payment.html'
    form_class = TransactionModelForm
    success_url = reverse_lazy('payment_history')

    def form_invalid(self, form):
        text = form.errors['__all__'][0]
        messages.add_message(self.request, messages.WARNING, text)
        return redirect(reverse_lazy('payment_history'))

    def form_valid(self, form):
        text = """Successfully send transaction request"""
        messages.add_message(self.request, messages.SUCCESS, text)
        return redirect(reverse_lazy('payment_history'))
