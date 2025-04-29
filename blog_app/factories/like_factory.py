from blog_app.factories.entry_factory import EntryFactory
from blog_app.models.like import Like
from factory import SubFactory
from factory.django import DjangoModelFactory
from user_app.factory.cryptek_user_factory import CryptekUserFactory


class LikeFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    entry = SubFactory(EntryFactory)

    class Meta:
        model = Like
