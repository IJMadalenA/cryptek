from django.contrib.admin import ModelAdmin, register

from library_tomb.models.tag import Tag


@register(Tag)
class TagAdmin(ModelAdmin):
    pass
