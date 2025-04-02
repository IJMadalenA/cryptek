from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField


# User model
class CryptekUser(AbstractUser):
    # Inherits fields from Django's AbstractUser
    # username
    # first_name
    # last_name
    # email
    # is_staff
    # is_active
    email_verified = BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Creates a profile automatically when saving a new user."""
        is_new = self.pk is None  # Verifica si el usuario es nuevo
        super().save(*args, **kwargs)  # Guarda el usuario primero

        if is_new:
            from user_app.models.profile import Profile  # Import within method to avoid circular import problems.

            Profile.objects.create(user=self)
