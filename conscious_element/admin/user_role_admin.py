from django.contrib.admin import register, ModelAdmin

from conscious_element.models.user_role import UserRole


@register(UserRole)
class UserRoleAdmin(ModelAdmin):
    pass
