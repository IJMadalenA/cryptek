from django.utils.text import slugify
from factory import Faker, LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText

from blog_app.models.entry import (Entry, EntryAnalytics, EntryReaction,
                                   EntryVersion)
from user_app.factory.cryptek_user_factory import CryptekUserFactory


class EntryFactory(DjangoModelFactory):
    author = SubFactory(CryptekUserFactory, username=FuzzyText(length=12))
    title = Faker(provider="sentence", nb_words=4)
    slug = LazyAttribute(lambda o: slugify(o.title))
    content = FuzzyText(length=120)
    status = FuzzyChoice([0, 1, 2])

    class Meta:
        model = Entry


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
