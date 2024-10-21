from django.contrib.admin import register, ModelAdmin

from conscious_element.models.profile import Profile


@register(Profile)
class ProfileAdmin(ModelAdmin):
    pass
