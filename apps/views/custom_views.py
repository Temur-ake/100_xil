from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView


class GetMixin:
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and (user.type == user.Type.OPERATOR or user.type == user.Type.ADMIN):
            return super().get(request, *args, **kwargs)
        text = f""" 
            Operator page ga faqat operatorlar va adminlar kiradi oshna 🤫
        """
        messages.add_message(request, messages.WARNING, message=text)
        return redirect(reverse_lazy('main-page'))


class CustomListView(GetMixin, ListView):
    pass


class CustomCreateView(GetMixin, CreateView):
    pass


class CustomUpdateView(GetMixin, UpdateView):
    pass
