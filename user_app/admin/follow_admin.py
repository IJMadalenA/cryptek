from django.contrib.admin import ModelAdmin, register
from user_app.models.follow import Follow


@register(Follow)
class FollowAdmin(ModelAdmin):
    pass
