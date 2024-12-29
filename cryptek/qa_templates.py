from django.test import TestCase
from factory.django import DjangoModelFactory


class BaseFactoryTest(TestCase):

    def setUp(self):
        if not hasattr(self, "Meta") or not hasattr(self.Meta, "factory"):
            self.skipTest("Skipping tests as no factory is defined in Meta.")
        if getattr(self.Meta, "abstract", False):
            self.skipTest("Skipping tests as this TestCase is marked abstract.")

        if not issubclass(self.Meta.factory, DjangoModelFactory):
            raise TypeError(
                "The factory defined in Meta is not a subclass of DjangoModelFactory"
            )

        self.model = self.Meta.factory._meta.model

    def test_create(self):
        instance = self.Meta.factory.create()
        self.assertIsInstance(instance, self.Meta.factory._meta.model)

    def test_create_multiple(self):
        instances = self.Meta.factory.create_batch(3)
        self.assertEqual(len(instances), 3)
        for instance in instances:
            self.assertIsInstance(instance, self.Meta.factory._meta.model)

    class Meta:
        abstract = True
        factory = None
