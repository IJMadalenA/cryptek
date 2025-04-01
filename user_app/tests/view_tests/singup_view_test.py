from django.test import TestCase

from cryptek.qa_templates import ClassBaseViewTestCase
from user_app.adapters import email_is_legitimate
from user_app.models.blocked_email_domain import BlockedEmailDomain, BlockedEmailDomainExtension


class SignupViewTestCase(ClassBaseViewTestCase):
    endpoint_name = "signup"
    is_authenticated = False


class EmailValidationTestCase(TestCase):

    def test_email_validator(self):
        email = "contact@test.io"
        email_check = email_is_legitimate(email)
        self.assertFalse(email_check)

    def test_block_email_is_saved(self):
        BlockedEmailDomainExtension.objects.all().delete()
        BlockedEmailDomain.objects.all().delete()

        email = "test@fake.gov.es"
        email_blocked = email_is_legitimate(email)
        self.assertFalse(email_blocked)
        self.assertEqual(BlockedEmailDomain.objects.count(), 1)
        self.assertEqual(BlockedEmailDomainExtension.objects.count(), 1)

        self.assertTrue(BlockedEmailDomain.objects.filter(domain="fake").exists())
        self.assertTrue(BlockedEmailDomainExtension.objects.filter(domain_extension="gov.es").exists())
