from factory import SubFactory
from factory.django import DjangoModelFactory

from library_tomb.factories.post_factory import PostFactory
from library_tomb.models.multimedia import Multimedia


class MultimediaFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)

    class Meta:
        model = Multimedia
