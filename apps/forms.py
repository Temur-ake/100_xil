from django.core.exceptions import ValidationError
from django.forms import CharField, ModelForm
from django.urls import reverse_lazy

from apps.models import User


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
