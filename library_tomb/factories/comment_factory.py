from factory import SubFactory
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from library_tomb.factories.post_factory import PostFactory
from library_tomb.models.comment import Comment


class CommentFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    post = SubFactory(PostFactory)

    class Meta:
        model = Comment
