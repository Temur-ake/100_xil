from django.db.models import Model, SlugField, CharField, DateTimeField
from django.db.models.functions import Now
from django.utils.text import slugify

from apps.utils import custom_slugify


class SlugBasedModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = custom_slugify(self.name)
        c = 1
        while self.__class__.objects.filter(slug=self.slug).exists():
            if self.slug.split('_')[-1].isdigit():
                self.slug = f"{self.slug.split('_')[0]}_{int(self.slug.split('_')[-1]) + c}"
            else:
                self.slug = f"{self.slug}_{c}"
            c += 1
        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

    def __str__(self):
        return self.name


class TimeBasedModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeSlugBased(SlugBasedModel, TimeBasedModel):
    class Meta:
        abstract = True
