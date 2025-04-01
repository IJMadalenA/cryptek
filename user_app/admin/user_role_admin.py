from django.contrib.admin import ModelAdmin, register

from user_app.models.user_role import UserRole


@register(UserRole)
class UserRoleAdmin(ModelAdmin):
    pass
