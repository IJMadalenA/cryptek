from django.db.models import (CASCADE, ImageField, Model, OneToOneField,
                              TextField)

from conscious_element.models.cryptek_user import CryptekUser


# Profile model
class Profile(Model):
    user = OneToOneField(CryptekUser, on_delete=CASCADE, related_name="profile")
    bio = TextField(blank=True)
    avatar = ImageField(upload_to="avatars/", blank=True, null=True)

    def str(self):
        return f"{self.user.username} Profile"
