from django.db.models import (CASCADE, BooleanField, CharField, DateTimeField,
                              ForeignKey, ImageField, IntegerField,
                              ManyToManyField, Model, OneToOneField, SlugField,
                              TextField)
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField

from conscious_element.models.cryptek_user import CryptekUser
from library_tomb.models.category import Category
from library_tomb.models.tag import Tag

STATUS = (
    (0, "Draft"),
    (1, "Published"),
    (2, "hidden"),
)


# Post model
class Post(Model):
    title = CharField(max_length=200)
    content = MarkdownxField()
    overview = TextField(
        blank=True,
        null=True,
        max_length=200,
    )
    author = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="posts")
    categories = ManyToManyField(Category, related_name="posts", blank=True)
    tags = ManyToManyField(Tag, related_name="posts", blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    status = IntegerField(
        choices=STATUS,
        default=0,
    )
    featured = BooleanField(default=False)
    publish_date = DateTimeField(blank=True, null=True)
    header_image = ImageField(upload_to="header_images/", blank=True, null=True)
    slug = SlugField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.author:
            self.author = CryptekUser.objects.first()
        super().save(*args, **kwargs)


# PostVersion model
class PostVersion(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name="versions")
    content = TextField()
    version_date = DateTimeField(auto_now_add=True)

    def str(self):
        return f"Version of {self.post.title} at {self.version_date}"


# PostReactions model
class PostReaction(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name="reactions")
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="reactions")
    reaction = CharField(max_length=50)  # e.g., 'like', 'love', 'haha', etc.

    def str(self):
        return f"{self.user} reacted to {self.post} with {self.reaction}"


# PostAnalytics model
class PostAnalytics(Model):
    post = OneToOneField(Post, on_delete=CASCADE, related_name="analytics")
    views = IntegerField(default=0)
    read_time = IntegerField(default=0)  # in seconds

    def str(self):
        return f"Analytics for {self.post.title}"
