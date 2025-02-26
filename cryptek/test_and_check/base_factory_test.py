from django.test import TestCase
from factory.django import DjangoModelFactory


class BaseFactoryTest(TestCase):
    """
    Base test case for testing factory implementations.
    """

    def setUp(self):
        """
        Prepares the test case for execution by performing checks and initialization based
        on the Meta attribute provided in the test class.
        """
        meta = getattr(self, "Meta", None)
        factory_cls = getattr(meta, "factory", None)

        if not meta or not factory_cls:
            self.skipTest("Skipping tests as no factory is defined in Meta.")
        if getattr(meta, "abstract", False):
            self.skipTest("Skipping tests as this TestCase is marked abstract.")
        if not issubclass(factory_cls, DjangoModelFactory):
            raise TypeError("The factory defined in Meta is not a subclass of DjangoModelFactory")

        self.model = factory_cls._meta.model

    def test_create(self):
        """Test creating a single instance of the model."""
        instance = self.Meta.factory.create()
        self.assertIsInstance(instance, self.model)

    def test_create_multiple(self):
        """Test creating multiple instances of the model."""
        instances = self.Meta.factory.create_batch(3)
        self.assertEqual(len(instances), 3)
        for instance in instances:
            self.assertIsInstance(instance, self.model)

    def test_str_representation(self):
        """Test the string representation of the model instance."""
        instance = self.Meta.factory.create()
        self.assertIsInstance(str(instance), str)

    class Meta:
        abstract = True
        factory = None
