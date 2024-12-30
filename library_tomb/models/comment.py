from django.db.models import (CASCADE, BooleanField, DateTimeField, ForeignKey,
                              Model, TextField)

from conscious_element.models.cryptek_user import CryptekUser
from library_tomb.models.post import Post


# Comment model
class Comment(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="comments")
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    active = BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
