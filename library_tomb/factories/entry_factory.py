from django.utils.text import slugify
from factory import SubFactory, post_generation
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from library_tomb.models.entry import (Entry, EntryAnalytics, EntryReaction,
                                       EntryVersion)


class EntryFactory(DjangoModelFactory):
    author = SubFactory(CryptekUserFactory)
    slug = None

    class Meta:
        model = Entry

    @post_generation
    def set_slug(self, create, extracted, **kwargs):
        """Force slug creation after the object is created if missing."""
        if not self.slug:
            self.slug = slugify(self.title)
        if create:
            self.save()


class EntryVersionFactory(DjangoModelFactory):
    entry = SubFactory(EntryFactory)

    class Meta:
        model = EntryVersion


class EntryReactionFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    entry = SubFactory(EntryFactory)

    class Meta:
        model = EntryReaction


class EntryAnalyticsFactory(DjangoModelFactory):
    entry = SubFactory(EntryFactory)

    class Meta:
        model = EntryAnalytics
