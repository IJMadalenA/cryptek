from factory.django import DjangoModelFactory
from factory import SubFactory
from library_tomb.factories.post_factory import PostFactory
from message_app.models.social_share import SocialShare


class SocialShareFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    class Meta:
        model = SocialShare
