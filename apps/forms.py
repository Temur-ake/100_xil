import re

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField

from apps.models import User, Order


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = 'phone', 'full_name', 'product'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return re.sub(r'[^\d]', '', phone)


class LoginRegisterModelForm(Form):
    phone = CharField(max_length=25)
    password = CharField(max_length=255)

    def get_user(self):
        return self._cache_user

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return re.sub(r'[^\d]', '', phone)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        self._cache_user, created = User.objects.get_or_create(phone=phone)
        if not created:
            self._cache_user = authenticate(phone=phone, password=password)

        if self._cache_user is None:
            raise ValidationError('User yoq')

        return cleaned_data


class PasswordChangeModelForm(ModelForm):
    class Meta:
        model = User
        fields = ()

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.pop("old_password")
        new_password = cleaned_data.pop("new_password")
        confirm_password = cleaned_data.pop("confirm_password")
        user = self.instance
        if user.check_password(old_password) and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
        else:
            raise ValidationError('Xato parol')
        return cleaned_data
