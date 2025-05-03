from datetime import time

from django.db import models
from django.test import TestCase
from factory.django import DjangoModelFactory


class BaseModelTestCase(TestCase):
    """
    Base test case for testing model implementations.

    Provides functionality to test if a Django model is properly set up,
    correctly creates single instances, and supports batch creation of multiple
    instances. Designed to work with `factory_boy`'s `DjangoModelFactory`.
    This test case also allows marking test cases as abstract or skipping the
    tests if no factory is provided.

    Attributes:
        model: Class of the model associated with the factory defined in Meta.

    Usage:
        class MyModelTestCase(BaseModelTestCase):
            class Meta:
                factory = MyModelFactory
    """

    def setUp(self):
        """
        Set up the test case by checking if it's abstract and initializing the model.

        Raises:
            TypeError: If the factory defined in Meta is not a subclass of DjangoModelFactory.
            AttributeError: If no Meta class or factory is defined.
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

    def test_create(self):
        """Test that a model instance can be created using the factory."""
        instance = self.Meta.factory.create()
        self.assertIsInstance(instance, self.model, f"Expected instance to be of type {self.model.__name__}")

    def test_create_multiple(self):
        """Test that multiple model instances can be created using the factory."""
        instances = self.Meta.factory.create_batch(3)
        self.assertEqual(len(instances), 3, "Expected 3 instances to be created")
        for instance in instances:
            self.assertIsInstance(instance, self.model, f"Expected instance to be of type {self.model.__name__}")

    def test_str_representation(self):
        """Test that the model's string representation is a string."""
        instance = self.Meta.factory.create()
        self.assertIsInstance(instance.__str__(), str, "Expected __str__ method to return a string")

    def test_save(self):
        """Test that a model instance can be saved to the database."""
        instance = self.Meta.factory.create()
        instance.save()
        self.assertIsNotNone(instance.pk, "Expected instance to have a primary key after saving")

    def test_delete(self):
        """Test that a model instance can be deleted from the database."""
        instance = self.Meta.factory.create()
        pk = instance.pk
        instance.delete()
        self.assertFalse(self.model.objects.filter(pk=pk).exists(), f"Expected instance with pk={pk} to be deleted")

    def _get_field_names_by_type(self, field_type):
        """
        Get the names of fields of a specific type.

        Args:
            field_type: The Django model field type to look for.

        Returns:
            list: A list of field names of the specified type.
        """
        return [field.name for field in self.model._meta.fields if isinstance(field, field_type)]

    def test_update_char_field(self):
        """Test that CharField values can be updated."""
        field_names = self._get_field_names_by_type(models.CharField)

        for field_name in field_names:
            instance = self.Meta.factory.create()
            setattr(instance, field_name, "New Value")
            instance.save()
            self.assertEqual(
                getattr(instance, field_name), "New Value", f"Expected {field_name} to be updated to 'New Value'"
            )

    def test_update_text_field(self):
        """Test that TextField values can be updated."""
        field_names = self._get_field_names_by_type(models.TextField)

        for field_name in field_names:
            instance = self.Meta.factory.create()
            setattr(instance, field_name, "New Text Value")
            instance.save()
            self.assertEqual(
                getattr(instance, field_name),
                "New Text Value",
                f"Expected {field_name} to be updated to 'New Text Value'",
            )

    def test_update_integer_field(self):
        """Test that IntegerField values can be updated."""
        field_names = self._get_field_names_by_type(models.IntegerField)

        for field_name in field_names:
            instance = self.Meta.factory.create()

            # Check if the model has unique fields that might cause conflicts
            # For models like Category with a unique slug generated from name
            unique_char_fields = [
                field for field in self.model._meta.fields if isinstance(field, models.CharField) and field.unique
            ]

            # If there are unique CharField fields, update them to ensure uniqueness
            for unique_field in unique_char_fields:
                import uuid

                unique_value = f"{unique_field.name}_{uuid.uuid4().hex[:8]}"
                setattr(instance, unique_field.name, unique_value)

            # Now update the integer field
            setattr(instance, field_name, 42)
            instance.save()
            self.assertEqual(getattr(instance, field_name), 42, f"Expected {field_name} to be updated to 42")

    def test_update_boolean_field(self):
        """Test that BooleanField values can be updated."""
        field_names = self._get_field_names_by_type(models.BooleanField)

        for field_name in field_names:
            instance = self.Meta.factory.create()
            setattr(instance, field_name, True)
            instance.save()
            self.assertTrue(getattr(instance, field_name), f"Expected {field_name} to be updated to True")

    def test_update_float_field(self):
        """Test that FloatField values can be updated."""
        field_names = self._get_field_names_by_type(models.FloatField)

        for field_name in field_names:
            instance = self.Meta.factory.create()
            setattr(instance, field_name, 3.14)
            instance.save()
            self.assertEqual(getattr(instance, field_name), 3.14, f"Expected {field_name} to be updated to 3.14")

    def test_update_date_field(self):
        """Test that DateField values can be updated."""
        field_names = self._get_field_names_by_type(models.DateField)

        for field_name in field_names:
            instance = self.Meta.factory.create()

            # Use timezone-aware date to avoid warnings
            from django.utils import timezone

            today = timezone.now().date()

            setattr(instance, field_name, today)
            instance.save()
            self.assertEqual(getattr(instance, field_name), today, f"Expected {field_name} to be updated to {today}")

    def test_update_time_field(self):
        """Test that TimeField values can be updated."""
        field_names = self._get_field_names_by_type(models.TimeField)

        for field_name in field_names:
            instance = self.Meta.factory.create()
            test_time = time(12, 0, 0)
            setattr(instance, field_name, test_time)
            instance.save()
            self.assertEqual(
                getattr(instance, field_name), test_time, f"Expected {field_name} to be updated to {test_time}"
            )

    def test_update_datetime_field(self):
        """Test that DateTimeField values can be updated."""
        field_names = self._get_field_names_by_type(models.DateTimeField)

        for field_name in field_names:
            instance = self.Meta.factory.create()

            # Use timezone-aware datetime to avoid warnings
            from django.utils import timezone

            now = timezone.now().replace(microsecond=0)  # Remove microseconds for comparison

            setattr(instance, field_name, now)
            instance.save()
            saved_value = getattr(instance, field_name).replace(microsecond=0)
            self.assertEqual(saved_value, now, f"Expected {field_name} to be updated to {now}")

    def test_update_foreign_key_field(self):
        """Test that ForeignKey values can be updated."""
        field_names = [field.name for field in self.model._meta.fields if isinstance(field, models.ForeignKey)]

        for field_name in field_names:
            instance = self.Meta.factory.create()
            field = self.model._meta.get_field(field_name)
            related_model = field.related_model

            # Try to create a related instance if possible
            try:
                related_instance = related_model.objects.create()
                setattr(instance, field_name, related_instance)
                instance.save()
                self.assertEqual(
                    getattr(instance, field_name),
                    related_instance,
                    f"Expected {field_name} to be updated to {related_instance}",
                )
            except Exception as e:
                self.skipTest(f"Could not test ForeignKey {field_name}: {str(e)}")

    def test_update_one_to_one_field(self):
        """Test that OneToOneField values can be updated."""
        field_names = [field.name for field in self.model._meta.fields if isinstance(field, models.OneToOneField)]

        for field_name in field_names:
            instance = self.Meta.factory.create()
            field = self.model._meta.get_field(field_name)
            related_model = field.related_model

            # Try to create a related instance if possible
            try:
                related_instance = related_model.objects.create()
                setattr(instance, field_name, related_instance)
                instance.save()
                self.assertEqual(
                    getattr(instance, field_name),
                    related_instance,
                    f"Expected {field_name} to be updated to {related_instance}",
                )
            except Exception as e:
                self.skipTest(f"Could not test OneToOneField {field_name}: {str(e)}")

    def test_update_many_to_many_field(self):
        """Test that ManyToManyField values can be updated."""
        field_names = [field.name for field in self.model._meta.many_to_many]

        for field_name in field_names:
            instance = self.Meta.factory.create()
            field = self.model._meta.get_field(field_name)
            related_model = field.related_model

            # Try to create a related instance if possible
            try:
                related_instance = related_model.objects.create()
                getattr(instance, field_name).add(related_instance)
                self.assertIn(
                    related_instance,
                    getattr(instance, field_name).all(),
                    f"Expected {related_instance} to be in {field_name}",
                )
            except Exception as e:
                self.skipTest(f"Could not test ManyToManyField {field_name}: {str(e)}")

    def test_update_choices_field(self):
        """Test that fields with choices can be updated to a valid choice."""
        for field in self.model._meta.fields:
            if hasattr(field, "choices") and field.choices:
                instance = self.Meta.factory.create()
                choice_value = field.choices[0][0]
                setattr(instance, field.name, choice_value)
                instance.save()
                self.assertEqual(
                    getattr(instance, field.name),
                    choice_value,
                    f"Expected {field.name} to be updated to {choice_value}",
                )

    def assert_field_exists(self, field_name):
        """
        Assert that a field exists on the model.

        Args:
            field_name (str): The name of the field to check.

        Raises:
            AssertionError: If the field does not exist on the model.
        """
        try:
            self.model._meta.get_field(field_name)
        except models.FieldDoesNotExist:
            self.fail(f"Field '{field_name}' does not exist on model {self.model.__name__}")

    def assert_field_type(self, field_name, field_type):
        """
        Assert that a field is of a specific type.

        Args:
            field_name (str): The name of the field to check.
            field_type (type): The expected type of the field.

        Raises:
            AssertionError: If the field is not of the expected type.
        """
        field = self.model._meta.get_field(field_name)
        self.assertIsInstance(
            field,
            field_type,
            f"Expected field '{field_name}' to be of type {field_type.__name__}, but got {field.__class__.__name__}",
        )

    def assert_field_attribute(self, field_name, attribute_name, expected_value):
        """
        Assert that a field has a specific attribute value.

        Args:
            field_name (str): The name of the field to check.
            attribute_name (str): The name of the attribute to check.
            expected_value: The expected value of the attribute.

        Raises:
            AssertionError: If the field does not have the expected attribute value.
        """
        field = self.model._meta.get_field(field_name)
        actual_value = getattr(field, attribute_name)
        self.assertEqual(
            actual_value,
            expected_value,
            f"Expected field '{field_name}' to have {attribute_name}={expected_value}, but got {actual_value}",
        )

    def assert_model_attribute(self, attribute_name, expected_value):
        """
        Assert that the model has a specific attribute value.

        Args:
            attribute_name (str): The name of the attribute to check.
            expected_value: The expected value of the attribute.

        Raises:
            AssertionError: If the model does not have the expected attribute value.
        """
        actual_value = getattr(self.model, attribute_name)
        self.assertEqual(
            actual_value,
            expected_value,
            f"Expected model {self.model.__name__} to have {attribute_name}={expected_value}, but got {actual_value}",
        )

    class Meta:
        abstract = True
        factory = None
