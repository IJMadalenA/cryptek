from django.contrib.admin import ModelAdmin, register
from user_app.models.profile import Profile


@register(Profile)
class ProfileAdmin(ModelAdmin):
    pass
