from factory.django import DjangoModelFactory

from user_app.models.user_role import UserRole


class UserRoleFactory(DjangoModelFactory):
    class Meta:
        model = UserRole
