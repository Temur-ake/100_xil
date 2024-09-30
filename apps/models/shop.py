from django.db.models import Model, TextField, ImageField, DateField, BooleanField, CharField, ForeignKey, RESTRICT, \
    CASCADE
from django.utils.translation import gettext_lazy as _

from apps.models.base import TimeBasedModel


class Concurs(Model):
    description = TextField(verbose_name='Sarlavhasi', null=True, blank=True)
    photo = ImageField(verbose_name='surati', upload_to='concurs/%Y/%m/%d')
    start_date = DateField(verbose_name='boshlash sanasi')
    end_date = DateField(verbose_name='tugash sanasi')
    is_active = BooleanField(verbose_name='Faolmi', default=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Competition')
        verbose_name_plural = _('Competitions')


class Payment(TimeBasedModel):
    account_number = CharField(max_length=200)
    user = ForeignKey('apps.User', CASCADE)
