from blog_app.factories.entry_factory import EntryFactory
from factory import SubFactory
from factory.django import DjangoModelFactory
from message_app.models.social_share import SocialShare


class SocialShareFactory(DjangoModelFactory):
    post = SubFactory(EntryFactory)

    class Meta:
        model = SocialShare
