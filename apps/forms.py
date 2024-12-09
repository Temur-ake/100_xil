import re

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Q, Sum
from django.forms import ModelForm, Form, CharField

from apps.models import User, Order, Stream, Product, Transaction, SiteSettings, District


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = 'full_name', 'product', 'quantity', 'stream', 'owner', 'phone', 'manzil', 'region', 'district'

    def clean_phone(self):
        phone: str = re.sub(r'[^\d]', '', self.cleaned_data.get('phone'))
        if len(phone) != 12 or not phone.startswith('998'):
            raise ValidationError("Noto'gri telefon raqam")
        phone = phone[-9:]
        return phone

    # def clean_quantity(self):
    #     quantity = self.cleaned_data.get('quantity')
    #     if quantity is None:
    #         quantity = 1
    #     return quantity


class OrderUpdateModelFormView(ModelForm):
    class Meta:
        model = Order
        fields = 'quantity', 'region', 'district', 'send_date', 'status', 'comment'

    def clean(self):
        cleaned_data = super().clean()
        order_id = self.instance.id
        data = {k: v for k, v in cleaned_data.items() if v}
        if cleaned_data['region']:
            data['region'] = data['region'].id
        if cleaned_data['district']:
            data['district'] = data['district'].id
        Order.objects.filter(id=order_id).update(**data)
        return cleaned_data


class CurrierOrderForm(Form):
    delivering = CharField(max_length=20)
    currier = CharField(max_length=20)
    orders = CharField(max_length=500, required=False)

    def clean(self):
        data = super().clean()
        status = data.get('delivering')
        currier_id = data.get('currier')

        order_idies = list(map(int, data.get('orders').split()))
        if status:
            qs = Order.objects.filter(id__in=order_idies)
            qs.update(status=status, currier_id=currier_id)
        return data


class StreamModelForm(ModelForm):
    class Meta:
        model = Stream
        fields = 'discount', 'name', 'product', 'owner'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean(self):
        data = super().clean()
        discount = data.get('discount')
        product_id = data.get('product').pk
        product_fee = Product.objects.filter(id=product_id).values_list('product_fee')[0][0] or 0
        if discount is None:
            data['discount'] = 0
        elif data['discount'] < 0:
            raise ValidationError("Chegirma musbat bo'lishi kerak")
        if data['discount'] > product_fee:
            raise ValidationError("Chegirma mahsulot to'lab beriladigan narxdan oshmasligi kerak")
        return data


class LoginRegisterModelForm(Form):
    phone = CharField(max_length=25)
    password = CharField(max_length=255)

    def get_user(self):
        return self._cache_user

    def clean(self):
        cleaned_data = super().clean()
        if ('phone' or 'password') not in cleaned_data.keys():
            raise ValidationError("Telefon va parol bo'sh bo'lishi mumkin emas")
        password = cleaned_data.get('password')
        phone: str = re.sub(r'[^\d]', '', cleaned_data.get('phone'))
        if len(phone) != 12 or not phone.startswith('998'):
            raise ValidationError('Incorrect password or phone number')
        phone = phone[-9:]
        user, created = User.objects.get_or_create(phone=phone[-9:])
        if created:
            user.set_password(password)
            user.save()

        user = authenticate(phone=phone, password=password)

        if user is None:
            raise ValidationError("Parol xato")
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


class CustomAdminAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = re.sub(r'[^\d]', '', username)
        if len(username) > 9:
            username = username[-9:]
        return username


class TransactionModelForm(ModelForm):
    class Meta:
        model = Transaction
        fields = 'card_number', 'amount', 'owner'

    def clean(self):
        cleaned_data = super().clean()
        amount = self.cleaned_data.get('amount')
        card_number = re.sub(r'[^\d]', '', self.cleaned_data.get('card_number'))
        owner = self.cleaned_data.get('owner')
        _user = User.objects.filter(id=owner.pk)
        user_balance = _user.values_list('balance', flat=True)[0]
        min_balance_amount = SiteSettings.objects.all().values_list('min_balance_amount', flat=True).first()
        limit_of_requests = Transaction.objects.aggregate(sum=Sum('amount', filter=Q(owner=owner) & Q(is_payed=False)))
        if len(card_number) < 16 or not card_number.isdigit():
            raise ValidationError("To'g'ri karta raqamini kiriting:")
        elif amount < min_balance_amount:
            raise ValidationError(f"Minimal o'tkazma summasi: {min_balance_amount} ")
        # elif amount > user_balance or (
        #         limit_of_requests.get('sum') and (limit_of_requests.get('sum') + amount) > user_balance):
        #     raise ValidationError(
        #         f'''
        #         Sizning balansingiz: {''.join([f"{v} " if k % 3 == 0 else f"{v}" for k, v in enumerate(str(user_balance))])}
        #         or limit of requests
        #         ''')
        elif amount > user_balance or (
                limit_of_requests.get('sum') and (limit_of_requests.get('sum') + amount) > user_balance):
            formatted_balance = "{:,}".format(user_balance).replace(",", " ")  # Use space as a thousands separator
            raise ValidationError(
                f'''
                Sizning balansingiz: {formatted_balance} so'm.
                Sizning so'rovlaringizning umumiy summasi ,  balansingizdan oshmasligi kerak.
                '''
            )
        Transaction.objects.create(**cleaned_data)
        return cleaned_data
