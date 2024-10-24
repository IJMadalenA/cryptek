from django.contrib.admin import ModelAdmin, register

from library_tomb.models.category import Category


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass
