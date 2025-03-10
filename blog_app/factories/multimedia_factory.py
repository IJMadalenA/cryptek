from factory import SubFactory
from factory.django import DjangoModelFactory

from library_tomb.factories.entry_factory import EntryFactory
from library_tomb.models.multimedia import Multimedia


class MultimediaFactory(DjangoModelFactory):
    post = SubFactory(EntryFactory)

    class Meta:
        model = Multimedia
