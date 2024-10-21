from django.db.models import Model, CharField, ForeignKey, TextField, CASCADE, ManyToManyField, DateTimeField, \
    BooleanField, OneToOneField, IntegerField

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
    content = TextField()
    overview = TextField()
    author = ForeignKey(CryptekUser, on_delete=CASCADE, related_name='posts')
    categories = ManyToManyField(Category, related_name='posts', blank=True)
    tags = ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_published = BooleanField(default=False)
    status = IntegerField(
        choices=STATUS,
        default=0,
    )
    featured = BooleanField()
    publish_date = DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def str(self):
        return self.title

# PostVersion model
class PostVersion(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='versions')
    content = TextField()
    version_date = DateTimeField(auto_now_add=True)

    def str(self):
        return f'Version of {self.post.title} at {self.version_date}'

# PostReactions model
class PostReaction(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='reactions')
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name='reactions')
    reaction = CharField(max_length=50)  # e.g., 'like', 'love', 'haha', etc.

    def str(self):
        return f'{self.user} reacted to {self.post} with {self.reaction}'

# PostAnalytics model
class PostAnalytics(Model):
    post = OneToOneField(Post, on_delete=CASCADE, related_name='analytics')
    views = IntegerField(default=0)
    read_time = IntegerField(default=0)  # in seconds

    def str(self):
        return f'Analytics for {self.post.title}'