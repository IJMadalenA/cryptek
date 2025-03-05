from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone


class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def check_token(self, user, token):
        # First, ensure the default checks pass
        if not super().check_token(user, token):
            return False

        # Check if token is expired
        # You can store your custom timeout in `settings.EMAIL_TOKEN_TIMEOUT` (in seconds)
        token_created_time = user.last_login or user.date_joined
        if (timezone.now() - token_created_time).total_seconds() > getattr(settings, "EMAIL_TOKEN_TIMEOUT", 86400):
            return False
        return True
