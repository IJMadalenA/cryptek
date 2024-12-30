from factory.django import DjangoModelFactory

from conscious_element.models.user_role import UserRole


class UserRoleFactory(DjangoModelFactory):
    class Meta:
        model = UserRole
