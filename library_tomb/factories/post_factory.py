from django.utils.text import slugify
from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from library_tomb.models.post import (Post, PostAnalytics, PostReaction,
                                      PostVersion)


class PostFactory(DjangoModelFactory):
    author = SubFactory(CryptekUserFactory)
    slug = None

    class Meta:
        model = Post

    @post_generation
    def set_slug(self, create, extracted, **kwargs):
        """Force slug creation after the object is created if missing."""
        if not self.slug:
            self.slug = slugify(self.title)
        if create:
            self.save()


class PostVersionFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)

    class Meta:
        model = PostVersion


class PostReactionFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = PostReaction


class PostAnalyticsFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)

    class Meta:
        model = PostAnalytics
