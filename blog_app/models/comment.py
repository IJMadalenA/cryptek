from blog_app.models.entry import Entry
from django.db.models import CASCADE, BooleanField, DateTimeField, ForeignKey, Model, TextField
from user_app.models.cryptek_user import CryptekUser


# Comment model
class Comment(Model):
    entry = ForeignKey(
        Entry,
        on_delete=CASCADE,
        related_name="comments",
        null=False,
        blank=False,
    )
    parent = ForeignKey(
        "self",
        on_delete=CASCADE,
        related_name="replies",
        null=True,
        blank=True,
    )
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="comments")
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    active = BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.user} on {self.entry}"
