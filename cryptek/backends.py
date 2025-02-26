from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailOrUsernameAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate using either
    their email or username along with their password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find the user by email or username
            user = User.objects.get(email=username) if "@" in username else User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Check if the provided password is correct
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
