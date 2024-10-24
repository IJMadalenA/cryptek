from django.contrib.admin import ModelAdmin, register

from conscious_element.models.user_role import UserRole


@register(UserRole)
class UserRoleAdmin(ModelAdmin):
    pass
