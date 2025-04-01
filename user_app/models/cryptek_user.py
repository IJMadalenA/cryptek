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
