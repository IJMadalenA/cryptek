from django.db.models import CASCADE, DateTimeField, ForeignKey, Model
from django.db.models.fields import BooleanField
from user_app.models.cryptek_user import CryptekUser


# Follow model
class Follow(Model):
    follower = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="following")
    following = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="followers")
    created_at = DateTimeField(auto_now_add=True)
    active = BooleanField(default=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
