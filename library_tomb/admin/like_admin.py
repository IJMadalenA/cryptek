from django.contrib.admin import register, ModelAdmin

from library_tomb.models.like import Like


@register(Like)
class LikeAdmin(ModelAdmin):
    pass
