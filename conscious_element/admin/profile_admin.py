from django.contrib.admin import ModelAdmin, register

from conscious_element.models.profile import Profile


@register(Profile)
class ProfileAdmin(ModelAdmin):
    pass
