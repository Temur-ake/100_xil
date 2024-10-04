from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _

from apps.models.base import TimeSlugBased


class Category(TimeSlugBased):
    photo = ImageField(verbose_name=_('Photo'), upload_to='categories/%Y/%m/%d')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
