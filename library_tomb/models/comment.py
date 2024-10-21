from django.db.models import Model, CASCADE, ForeignKey, TextField, DateTimeField, BooleanField

from library_tomb.models.post import Post


# Comment model
class Comment(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    user = ForeignKey(User, on_delete=CASCADE, related_name='comments')
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    active = BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def str(self):
        return f'Comment by {self.user} on {self.post}'