from django.db.models import CASCADE, ImageField, Model, OneToOneField, TextField
from django.db.models.fields import DateField
from rest_framework.fields import CharField

from user_app.models.cryptek_user import CryptekUser


# Profile model
class Profile(Model):
    user = OneToOneField(CryptekUser, on_delete=CASCADE, related_name="profile")
    bio = TextField(blank=True)
    avatar = ImageField(upload_to="avatars/", blank=True, null=True)
    location = CharField(max_length=120)
    birth_date = DateField(blank=True, null=True)
    website = CharField(max_length=120)
    phone_number = CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} Profile"

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return None

    def get_bio(self):
        if self.bio:
            return self.bio
        return None
