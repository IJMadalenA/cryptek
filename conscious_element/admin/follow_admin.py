from django.contrib.admin import ModelAdmin, register

from conscious_element.models.follow import Follow


@register(Follow)
class FollowAdmin(ModelAdmin):
    pass
