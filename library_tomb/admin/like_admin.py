from django.contrib.admin import ModelAdmin, register

from library_tomb.models.like import Like


@register(Like)
class LikeAdmin(ModelAdmin):
    pass
