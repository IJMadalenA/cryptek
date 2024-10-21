from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from conscious_element.models.cryptek_user import CryptekUser


@register(CryptekUser)
class CryptekUserAdmin(UserAdmin):
    model = CryptekUser
