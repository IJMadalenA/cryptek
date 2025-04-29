from blog_app.factories.entry_factory import EntryFactory
from blog_app.models.multimedia import Multimedia
from factory import SubFactory
from factory.django import DjangoModelFactory


class MultimediaFactory(DjangoModelFactory):
    post = SubFactory(EntryFactory)

    class Meta:
        model = Multimedia
