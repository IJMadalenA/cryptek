from datetime import date, datetime, time

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
    """

    def setUp(self):
        if getattr(self.Meta, "abstract", False):
            self.skipTest("Skipping tests as this TestCase is marked abstract.")

        if not issubclass(self.Meta.factory, DjangoModelFactory):
            raise TypeError("The factory defined in Meta is not a subclass of DjangoModelFactory")
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

    def test_save(self):
        instance = self.Meta.factory.create()
        instance.save()
        self.assertIsNotNone(instance.pk)

    def test_delete(self):
        instance = self.Meta.factory.create()
        instance.delete()
        self.assertFalse(self.model.objects.filter(pk=instance.pk).exists())

    def test_update_str_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, str):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, "New Value")
                instance.save()
                self.assertEqual(getattr(instance, field.name), "New Value")

    def test_update_int_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, int):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, 5)
                instance.save()
                self.assertEqual(getattr(instance, field.name), 5)

    def test_update_bool_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, bool):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, True)
                instance.save()
                self.assertEqual(getattr(instance, field.name), True)

    def test_update_float_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, float):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, 5.0)
                instance.save()
                self.assertEqual(getattr(instance, field.name), 5.0)

    def test_update_date_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, date):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, date.today())
                instance.save()
                self.assertEqual(getattr(instance, field.name), date.today())

    def test_update_time_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, time):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, time(12, 0, 0))
                instance.save()
                self.assertEqual(getattr(instance, field.name), time(12, 0, 0))

    def test_update_datetime_field(self):
        for field in self.model._meta.fields:
            if isinstance(field, datetime):
                instance = self.Meta.factory.create()
                setattr(instance, field.name, datetime.now())
                instance.save()
                self.assertEqual(getattr(instance, field.name), datetime.now())

    def test_update_one_to_one_field(self):
        for field in self.model._meta.fields:
            if field.is_relation and field.one_to_one:
                instance = self.Meta.factory.create()
                related_instance = self.Meta.factory.create()
                setattr(instance, field.name, related_instance)
                instance.save()
                self.assertEqual(getattr(instance, field.name), related_instance)

    def test_update_many_to_many_field(self):
        for field in self.model._meta.fields:
            if field.is_relation and field.many_to_many:
                instance = self.Meta.factory.create()
                related_instance = self.Meta.factory.create()
                getattr(instance, field.name).add(related_instance)
                instance.save()
                self.assertIn(related_instance, getattr(instance, field.name).all())

    def test_update_choices_field(self):
        for field in self.model._meta.fields:
            if field.choices:
                instance = self.Meta.factory.create()
                setattr(instance, field.name, field.choices[0][0])
                instance.save()
                self.assertEqual(getattr(instance, field.name), field.choices[0][0])

    class Meta:
        abstract = True
        factory = None
