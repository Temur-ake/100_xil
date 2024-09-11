from django.db.models import ImageField

from apps.models.base import TimeSlugBased


class Category(TimeSlugBased):
    photo = ImageField(upload_to='categories/%Y/%m/%d')