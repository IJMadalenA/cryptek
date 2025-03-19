from factory import Sequence
from factory.django import DjangoModelFactory

from blog_app.models.category import Category


class CategoryFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"Category {n}")

    class Meta:
        model = Category
