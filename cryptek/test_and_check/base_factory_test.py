import inspect

from django.test import TestCase
from factory import Faker, LazyAttribute, LazyFunction, Sequence, SubFactory, Trait, post_generation
from factory.django import DjangoModelFactory


class BaseFactoryTest(TestCase):
    """
    Base test case for testing factory implementations.

    This class provides methods for testing factory creation, batch creation,
    string representation, and advanced factory features like traits, sequences,
    and post-generation hooks.

    Usage:
        class MyFactoryTestCase(BaseFactoryTest):
            class Meta:
                factory = MyFactory
    """

    def setUp(self):
        """
        Prepares the test case for execution by performing checks and initialization based
        on the Meta attribute provided in the test class.

        Raises:
            AttributeError: If no Meta class or factory is defined.
            TypeError: If the factory defined in Meta is not a subclass of DjangoModelFactory.
        """
        meta = getattr(self, "Meta", None)
        if not meta:
            raise AttributeError("No Meta class defined. Please define a Meta class with a factory attribute.")

        if getattr(meta, "abstract", False):
            self.skipTest("Skipping tests as this TestCase is marked abstract.")

        factory_cls = getattr(meta, "factory", None)
        if not factory_cls:
            raise AttributeError("No factory defined in Meta. Please define a factory attribute in the Meta class.")

        if not issubclass(factory_cls, DjangoModelFactory):
            raise TypeError("The factory defined in Meta is not a subclass of DjangoModelFactory")

        self.model = factory_cls._meta.model
        self.factory = factory_cls

    def test_create(self):
        """Test creating a single instance of the model."""
        instance = self.factory.create()
        self.assertIsInstance(instance, self.model, 
                             f"Expected instance to be of type {self.model.__name__}")
        self.assertIsNotNone(instance.pk, 
                            "Expected instance to have a primary key after creation")

    def test_create_multiple(self):
        """Test creating multiple instances of the model."""
        batch_size = 3
        instances = self.factory.create_batch(batch_size)
        self.assertEqual(len(instances), batch_size, 
                        f"Expected {batch_size} instances to be created")

        # Check that all instances are of the correct type
        for instance in instances:
            self.assertIsInstance(instance, self.model, 
                                 f"Expected instance to be of type {self.model.__name__}")

        # Check that all instances have unique primary keys
        pks = [instance.pk for instance in instances]
        self.assertEqual(len(pks), len(set(pks)), 
                        "Expected all instances to have unique primary keys")

    def test_build(self):
        """Test building a model instance without saving it to the database."""
        instance = self.factory.build()
        self.assertIsInstance(instance, self.model, 
                             f"Expected instance to be of type {self.model.__name__}")
        self.assertIsNone(instance.pk, 
                         "Expected instance to not have a primary key after building")

    def test_stub(self):
        """Test creating a stub with the factory's attributes."""
        try:
            stub = self.factory.stub()
            # Check that the stub has all the attributes defined in the factory
            for key, value in self.factory._meta.declarations.items():
                self.assertTrue(hasattr(stub, key), 
                               f"Expected stub to have attribute '{key}'")
        except NotImplementedError:
            self.skipTest("Factory does not support stub creation")

    def test_str_representation(self):
        """Test the string representation of the model instance."""
        instance = self.factory.create()
        self.assertIsInstance(str(instance), str, 
                             "Expected __str__ method to return a string")
        self.assertTrue(len(str(instance)) > 0, 
                       "Expected __str__ method to return a non-empty string")

    def test_factory_attributes(self):
        """Test that the factory defines all required model fields."""
        instance = self.factory.build()

        # Get all non-nullable fields from the model
        required_fields = []
        for field in self.model._meta.fields:
            if not field.null and not field.blank and not field.has_default() and not field.primary_key:
                required_fields.append(field.name)

        # Check that all required fields are defined in the factory
        for field_name in required_fields:
            try:
                value = getattr(instance, field_name)
                self.assertIsNotNone(value, 
                                   f"Expected factory to define required field '{field_name}'")
            except AttributeError:
                self.fail(f"Factory does not define required field '{field_name}'")

    def test_sequences(self):
        """Test that sequences in the factory generate unique values."""
        # Find all sequence declarations in the factory
        sequence_attrs = []
        for key, value in self.factory._meta.declarations.items():
            if isinstance(value, Sequence):
                sequence_attrs.append(key)

        if not sequence_attrs:
            self.skipTest("Factory does not use sequences")

        # Create multiple instances and check that sequence values are unique
        instances = self.factory.create_batch(3)
        for attr in sequence_attrs:
            values = [getattr(instance, attr) for instance in instances]
            self.assertEqual(len(values), len(set(values)), 
                            f"Expected sequence '{attr}' to generate unique values")

    def test_lazy_attributes(self):
        """Test that lazy attributes in the factory are evaluated correctly."""
        # Find all lazy attribute declarations in the factory
        lazy_attrs = []
        for key, value in self.factory._meta.declarations.items():
            if isinstance(value, LazyAttribute) or isinstance(value, LazyFunction):
                lazy_attrs.append(key)

        if not lazy_attrs:
            self.skipTest("Factory does not use lazy attributes")

        # Create an instance and check that lazy attributes are evaluated
        instance = self.factory.create()
        for attr in lazy_attrs:
            self.assertIsNotNone(getattr(instance, attr), 
                               f"Expected lazy attribute '{attr}' to be evaluated")

    def test_subfactories(self):
        """Test that subfactories in the factory create related instances."""
        # Find all subfactory declarations in the factory
        subfactory_attrs = []
        for key, value in self.factory._meta.declarations.items():
            if isinstance(value, SubFactory):
                subfactory_attrs.append(key)

        if not subfactory_attrs:
            self.skipTest("Factory does not use subfactories")

        # Create an instance and check that subfactories create related instances
        instance = self.factory.create()
        for attr in subfactory_attrs:
            related_instance = getattr(instance, attr)
            self.assertIsNotNone(related_instance, 
                               f"Expected subfactory '{attr}' to create a related instance")
            self.assertIsNotNone(related_instance.pk, 
                               f"Expected related instance from subfactory '{attr}' to be saved")

    def test_faker_providers(self):
        """Test that Faker providers in the factory generate valid data."""
        # Find all Faker declarations in the factory
        faker_attrs = []
        for key, value in self.factory._meta.declarations.items():
            if isinstance(value, Faker):
                faker_attrs.append(key)

        if not faker_attrs:
            self.skipTest("Factory does not use Faker providers")

        # Create an instance and check that Faker providers generate data
        instance = self.factory.create()
        for attr in faker_attrs:
            self.assertIsNotNone(getattr(instance, attr), 
                               f"Expected Faker provider '{attr}' to generate data")

    def test_traits(self):
        """Test that traits in the factory modify instances correctly."""
        # Find all trait declarations in the factory
        traits = {}
        for key, value in inspect.getmembers(self.factory):
            if isinstance(value, Trait):
                traits[key] = value

        if not traits:
            self.skipTest("Factory does not define traits")

        # Create an instance with each trait and check that it's modified correctly
        for trait_name, trait in traits.items():
            instance = self.factory.create(**{trait_name: True})
            self.assertIsInstance(instance, self.model, 
                                 f"Expected instance with trait '{trait_name}' to be of type {self.model.__name__}")

            # Check that the trait's attributes are set on the instance
            for attr, value in trait.attrs.items():
                if callable(value):
                    # Skip callable values as they might depend on the instance
                    continue
                self.assertEqual(getattr(instance, attr), value, 
                                f"Expected trait '{trait_name}' to set '{attr}' to {value}")

    def test_post_generation_hooks(self):
        """Test that post-generation hooks in the factory are called."""
        # Find all post-generation hooks in the factory
        post_gen_attrs = []
        for key, value in self.factory._meta.declarations.items():
            # Check if the value is a post_generation decorator
            # post_generation is a decorator, not a type, so we can't use isinstance
            # Instead, check if it has the attribute that indicates it's a post_generation
            if hasattr(value, 'decorator') and value.decorator is post_generation:
                post_gen_attrs.append(key)

        if not post_gen_attrs:
            self.skipTest("Factory does not define post-generation hooks")

        # Create an instance and check that post-generation hooks are called
        instance = self.factory.create()
        for attr in post_gen_attrs:
            # We can't directly test that the hook was called, but we can check that the attribute exists
            self.assertTrue(hasattr(instance, attr), 
                           f"Expected post-generation hook '{attr}' to be called")

    def assert_factory_attribute(self, attribute_name, expected_type=None):
        """
        Assert that the factory defines a specific attribute.

        Args:
            attribute_name (str): The name of the attribute to check.
            expected_type (type, optional): The expected type of the attribute.

        Raises:
            AssertionError: If the factory does not define the attribute or it's not of the expected type.
        """
        self.assertTrue(attribute_name in self.factory._meta.declarations, 
                       f"Expected factory to define attribute '{attribute_name}'")

        if expected_type:
            attr = self.factory._meta.declarations[attribute_name]
            self.assertIsInstance(attr, expected_type, 
                                 f"Expected attribute '{attribute_name}' to be of type {expected_type.__name__}")

    def assert_factory_creates_valid_instance(self, **kwargs):
        """
        Assert that the factory creates a valid instance with the given attributes.

        Args:
            **kwargs: Attributes to set on the instance.

        Returns:
            The created instance.

        Raises:
            AssertionError: If the factory does not create a valid instance.
        """
        instance = self.factory.create(**kwargs)
        self.assertIsInstance(instance, self.model, 
                             f"Expected instance to be of type {self.model.__name__}")
        self.assertIsNotNone(instance.pk, 
                            "Expected instance to have a primary key after creation")

        # Check that the attributes are set correctly
        for key, value in kwargs.items():
            self.assertEqual(getattr(instance, key), value, 
                            f"Expected attribute '{key}' to be set to {value}")

        return instance

    class Meta:
        abstract = True
        factory = None
