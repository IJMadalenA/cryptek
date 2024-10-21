from django.db.models import Model, ForeignKey, CASCADE, CharField, IntegerField

from library_tomb.models.post import Post


class SocialShare(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='social_shares')
    platform = CharField(max_length=100)  # e.g., 'Facebook', 'Twitter', etc.
    share_count = IntegerField(default=0)

    def str(self):
        return f'{self.post.title} shared on {self.platform}'
