from blog_app.models.entry import Entry
from django.db.models import CASCADE, CharField, DateTimeField, ForeignKey, Model
from user_app.models.cryptek_user import CryptekUser


class Like(Model):
    LIKE = "like"
    DISLIKE = "dislike"
    TYPE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    entry = ForeignKey(Entry, on_delete=CASCADE, related_name="likes")
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="likes")
    type = CharField(max_length=7, choices=TYPE_CHOICES, default=LIKE)
    created_at = DateTimeField(auto_now_add=True)
    user_agent = CharField(max_length=255, blank=True, null=True)
    ip_address = CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return f"{self.user} {self.type}s {self.entry}"
