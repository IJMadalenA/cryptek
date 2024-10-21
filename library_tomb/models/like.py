from django.db.models import Model, CASCADE, ForeignKey, DateTimeField

from library_tomb.models.post import Post


class Like(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='likes')
    user = ForeignKey(User, on_delete=CASCADE, related_name='likes')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
