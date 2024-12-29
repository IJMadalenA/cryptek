from factory import SubFactory
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from library_tomb.models.post import Post


class PostFactory(DjangoModelFactory):
    author = SubFactory(CryptekUserFactory)

    class Meta:
        model = Post
