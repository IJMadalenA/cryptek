from factory import Sequence
from factory.django import DjangoModelFactory

from library_tomb.models.tag import Tag


class TagFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"Tag_{n}")

    class Meta:
        model = Tag
