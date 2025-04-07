import logging

from cloudinary import CloudinaryImage
from cloudinary.exceptions import Error as CloudinaryError
from cloudinary.uploader import upload
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    IntegerField,
    ManyToManyField,
    Model,
    OneToOneField,
    SlugField,
    TextField,
    URLField,
)
from django.urls import reverse
from django.utils.text import slugify
from markdownx.models import MarkdownxField

from blog_app.models.category import Category
from blog_app.models.tag import Tag
from user_app.models.cryptek_user import CryptekUser

logger = logging.getLogger(__name__)

STATUS = (
    (0, "Draft"),
    (1, "Published"),
    (2, "hidden"),
)


# Entry model
class Entry(Model):
    title = CharField(max_length=100)
    content = MarkdownxField()
    overview = TextField(
        blank=True,
        null=True,
        max_length=200,
    )
    author = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="entries")
    categories = ManyToManyField(Category, related_name="entries", blank=True)
    tags = ManyToManyField(Tag, related_name="entries", blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    status = IntegerField(
        choices=STATUS,
        default=0,
    )
    featured = BooleanField(default=False)
    publish_date = DateTimeField(blank=True, null=True)
    header_image = ImageField(upload_to="header_images/", blank=True, null=True)
    cdn_image_url = URLField(blank=True, null=True, unique=True)
    cdn_image_public_id = CharField(max_length=200, blank=True, null=True)
    slug = SlugField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Entries"
        get_latest_by = "created_at"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_app:entry_detail", kwargs={"slug": self.slug})

    def get_full_url(self):
        return f"https://ijmadalena.com/{
        reverse('blog_app:entry_detail', kwargs={'slug': self.slug})
        }"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.author or self.author.is_anonymous:
            self.author = kwargs.get("user", self.author)
        if self.header_image:
            try:
                cdn_response = upload(self.header_image, public_id=self.slug)
                self.cdn_image_url = cdn_response.get("secure_url")
                self.cdn_image_public_id = cdn_response.get("public_id")
            except CloudinaryError as e:
                logger.error(f"Cloudinary upload failed: {e}")
                self.cdn_image_url = None

        super().save(*args, **kwargs)

    def get_header_image_optimized(self):
        if self.cdn_image_url:
            image = CloudinaryImage(
                public_id=self.cdn_image_public_id,
            ).build_url(
                crop="fill",
                quality="auto:good",
                fetch_format="auto",
            )
            return image

    def get_all_comments(self):
        return self.comments.filter(active=True)

    @property
    def like_count(self):
        return self.likes.filter(type="like").count()

    @property
    def dislike_count(self):
        return self.likes.filter(type="dislike").count()


# EntryVersion model
class EntryVersion(Model):
    entry = ForeignKey(Entry, on_delete=CASCADE, related_name="versions")
    content = TextField()
    version_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version of {self.entry.title} at {self.version_date}"


# EntryReactions model
class EntryReaction(Model):
    entry = ForeignKey(Entry, on_delete=CASCADE, related_name="reactions")
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="reactions")
    reaction = CharField(max_length=50)  # e.g., 'like', 'love', 'haha', etc.

    def __str__(self):
        return f"{self.user} reacted to {self.entry} with {self.reaction}"


# EntryAnalytics model
class EntryAnalytics(Model):
    entry = OneToOneField(Entry, on_delete=CASCADE, related_name="analytics")
    views = IntegerField(default=0)
    read_time = IntegerField(default=0)  # in seconds

    def __str__(self):
        return f"Analytics for {self.entry.title}"
