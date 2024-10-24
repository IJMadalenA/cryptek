from django.db.models import CASCADE, CharField, FileField, ForeignKey, Model

from library_tomb.models.post import Post


# Multimedia model
class Multimedia(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name="media")
    file = FileField(upload_to="media/")
    media_type = CharField(max_length=50)  # e.g., 'image', 'video', 'audio'

    def str(self):
        return f"Media for {self.post.title}"
