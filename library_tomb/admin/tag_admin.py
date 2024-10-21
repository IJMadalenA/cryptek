from django.contrib.admin import register, ModelAdmin

from library_tomb.models.tag import Tag


@register(Tag)
class TagAdmin(ModelAdmin):
    pass
