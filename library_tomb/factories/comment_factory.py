from factory import SubFactory
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from library_tomb.factories.entry_factory import EntryFactory
from library_tomb.models.comment import Comment


class CommentFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    entry = SubFactory(EntryFactory)

    class Meta:
        model = Comment
