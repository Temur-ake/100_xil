from django.db.models import Model, SlugField, CharField, DateTimeField
from django.db.models.functions import Now
from django.utils.text import slugify


class SlugBasedModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

    def __str__(self):
        return self.name


class TimeBasedModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True, db_default=Now())

    class Meta:
        abstract = True


class TimeSlugBased(SlugBasedModel, TimeBasedModel):
    class Meta:
        abstract = True
