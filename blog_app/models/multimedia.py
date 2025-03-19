from django.db.models import CASCADE, CharField, FileField, ForeignKey, Model

from blog_app.models.entry import Entry


# Multimedia model
class Multimedia(Model):
    post = ForeignKey(Entry, on_delete=CASCADE, related_name="media")
    file = FileField(upload_to="media/")
    media_type = CharField(max_length=50)  # e.g., 'image', 'video', 'audio'

    def __str__(self):
        return f"Media for {self.post.title}"
