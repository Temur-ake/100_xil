import re

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField

from apps.models import User, Order, Stream, Product


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = 'phone', 'full_name', 'product', 'stream', 'owner'

    def clean_phone(self):
        phone: str = re.sub(r'[^\d]', '', self.cleaned_data.get('phone'))
        if len(phone) != 12 or not phone.startswith('998'):
            raise ValidationError('Incorrect password or phone number')
        return phone


class StreamModelForm(ModelForm):
    class Meta:
        model = Stream
        fields = 'name', 'product', 'discount', 'owner'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount < 0:
            raise ValidationError('Discount is not valid')
        return discount

    def clean(self):
        data = super().clean()
        discount = data.get('discount')
        product_id = data.get('product').pk
        product_fee = Product.objects.filter(id=product_id).values_list('product_fee')[0][0]
        if discount > product_fee:
            raise ValidationError('Discount must not be exceed than product fee')
        return data


class LoginRegisterModelForm(Form):
    phone = CharField(max_length=25)
    password = CharField(max_length=255)

    def get_user(self):
        return self._cache_user

    def clean_phone(self):
        phone: str = re.sub(r'[^\d]', '', self.cleaned_data.get('phone'))
        if len(phone) != 12 or not phone.startswith('998'):
            raise ValidationError('Incorrect password or phone number')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        if not phone or not password:
            raise ValidationError('Phone and password cannot be blank')
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.set_password(password)
            user.save()

        user = authenticate(phone=phone, password=password)

        if user is None:
            raise ValidationError('Password xato')
        self._cache_user = user
        return cleaned_data


class PasswordChangeModelForm(ModelForm):
    old_password = CharField(max_length=255)
    new_password = CharField(max_length=255)
    confirm_password = CharField(max_length=255)

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
