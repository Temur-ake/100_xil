from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from apps.models import Category, Product


# Register your models here.
@admin.register(Category)
class CategoryModelAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'id', 'name', 'price', 'quantity', 'gfvhb'
    list_display_links = 'name',

    @admin.display(description='Rasmi')
    def gfvhb(self, obj: Product):
        img = obj.photo
        if img:
            return mark_safe(f"<img src={img.url} alt='img' width='60px' height='60px'")
        return 'None'
