from django.test import TestCase
from factory.django import DjangoModelFactory


class BaseFactoryTest(TestCase):
    """
    Base test case for testing factory implementations.

    Provides functionality to test if a Django model factory is properly set up,
    correctly creates single instances, and supports batch creation of multiple
    instances. Designed to work with `factory_boy`'s `DjangoModelFactory`.
    This test case also allows marking test cases as abstract or skipping the
    tests if no factory is provided.

    Attributes:
        model: Class of the model associated with the factory defined in Meta.
    """

    def setUp(self):
        """
        setUp(self)

        Prepares the test case for execution by performing checks and initialization based
        on the Meta attribute provided in the test class. It ensures that a compatible
        factory and model are defined before executing the tests.

        Raises
        ------
        TypeError
            If the 'factory' defined in the Meta attribute is not a subclass of
            DjangoModelFactory.

        Skips
        -----
        If the Meta attribute does not define a 'factory' property or if the 'abstract'
        attribute of Meta is set to True, the test will be skipped to prevent execution.

        Notes
        -----
        This method verifies that:
        - 'Meta' and its 'factory' attribute are defined in the test class.
        - The 'abstract' field in the Meta attribute determines whether the tests
          should be executed.
        - The factory must be a subclass of DjangoModelFactory for compatibility.

        After validation, the corresponding model for the factory is set to
        self.model for further use.
        """
        if not hasattr(self, "Meta") or not hasattr(self.Meta, "factory"):
            self.skipTest("Skipping tests as no factory is defined in Meta.")
        if getattr(self.Meta, "abstract", False):
            self.skipTest("Skipping tests as this TestCase is marked abstract.")

        if not self.Meta.factory or not issubclass(self.Meta.factory, DjangoModelFactory):
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

    def test_str_representation(self):
        instance = self.Meta.factory.create()
        self.assertIsInstance(instance.__str__(), str)

    class Meta:
        abstract = True
        factory = None
