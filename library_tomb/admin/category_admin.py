from django.contrib.admin import register, ModelAdmin

from library_tomb.models.category import Category


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass
