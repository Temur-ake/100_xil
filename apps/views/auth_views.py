from django.contrib import messages, admin
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, FormView

from apps.forms import PasswordChangeModelForm, LoginRegisterModelForm
from apps.models import User, Region, District, Order


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/users/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    fields = 'first_name', 'last_name', 'address', 'telegram_id', 'about', 'district'
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
            Malumotlarni to'liq to'ldiring
                            """
        messages.add_message(self.request, messages.WARNING, text)
        return super().form_invalid(form)


class UserPhotoUpdateView(UpdateView):
    template_name = 'apps/users/profile_settings.html'
    fields = 'photo',
    success_url = reverse_lazy('main-page')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordUpdateView(UpdateView):
    template_name = 'apps/users/profile_settings.html'
    form_class = PasswordChangeModelForm
    success_url = reverse_lazy('main-page')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        login(self.request, self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('pass-settings')


class LoginRegisterView(FormView):
    template_name = 'apps/auth/login-register.html'
    form_class = LoginRegisterModelForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.is_operator():
            return redirect('operator')
        return redirect('main-page')

    def form_invalid(self, form):
        text = form.errors['__all__'][0]
        messages.add_message(self.request, messages.WARNING, text)
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main-page')
        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')


def get_districts_by_region(request, region_id):
    districts = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


class SuccessValijonTemplateView(TemplateView):
    template_name = 'admin/apps/valijon.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        })
        return context
