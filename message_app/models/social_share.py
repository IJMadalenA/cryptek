from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Model

from blog_app.models.entry import Entry


class SocialShare(Model):
    post = ForeignKey(Entry, on_delete=CASCADE, related_name="social_shares")
    platform = CharField(max_length=100)  # e.g., 'Facebook', 'Twitter', etc.
    share_count = IntegerField(default=0)

    def __str__(self):
        return f"{self.post.title} shared on {self.platform}"
