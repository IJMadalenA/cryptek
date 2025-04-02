from unittest.mock import MagicMock, patch

import dns.resolver
import requests
from django.test import TestCase

from cryptek.qa_templates import ClassBaseViewTestCase
from user_app.adapters import email_is_legitimate
from user_app.models.blocked_email_domain import BlockedEmailDomain, BlockedEmailDomainExtension


class SignupViewTestCase(ClassBaseViewTestCase):
    endpoint_name = "signup"
    is_authenticated = False


class EmailValidationTestCase(TestCase):

    def setUp(self):
        """Clean the database before each test."""
        BlockedEmailDomain.objects.all().delete()
        BlockedEmailDomainExtension.objects.all().delete()

    @patch("user_app.adapters.requests.get")
    @patch("dns.resolver.resolve")  # 🔹 Mockeamos la validación MX
    def test_valid_email(self, mock_dns, mock_hunter):
        """A valid email should be accepted and not blocked."""
        mock_hunter.return_value.json.return_value = {
            "data": {"disposable": False, "smtp_check": True, "mx_records": True, "score": 90, "status": "valid"}
        }
        mock_dns.return_value = [MagicMock()]  # 🔹 Simulamos que hay registros MX

        email = "user@legit.com"
        result = email_is_legitimate(email)

        self.assertTrue(result)  # Ahora debería pasar
        self.assertFalse(BlockedEmailDomain.objects.filter(domain="legit.com").exists())

    @patch("user_app.adapters.requests.get")
    def test_disposable_email_is_blocked(self, mock_hunter):
        """A disposable email must be blocked and stored in the DB."""
        mock_hunter.return_value.json.return_value = {
            "data": {"disposable": True, "smtp_check": False, "mx_records": False, "score": 20, "status": "invalid"}
        }

        email = "temp@trashmail.com"
        result = email_is_legitimate(email)
        self.assertFalse(result)
        self.assertTrue(BlockedEmailDomain.objects.filter(domain="trashmail").exists())

    @patch("user_app.adapters.requests.get")
    @patch("dns.resolver.resolve")
    def test_email_without_mx_records_is_blocked(self, mock_dns, mock_hunter):
        """An email without valid MX records must be blocked."""
        mock_hunter.return_value.json.return_value = {
            "data": {"disposable": False, "smtp_check": True, "mx_records": True, "score": 85, "status": "valid"}
        }
        mock_dns.side_effect = dns.resolver.NoAnswer  # Simula error en la resolución DNS

        email = "no-mx@invalid.com"
        result = email_is_legitimate(email)
        self.assertFalse(result)
        self.assertTrue(BlockedEmailDomain.objects.filter(domain="invalid").exists())

    @patch("user_app.adapters.requests.get")
    @patch("dns.resolver.resolve")
    def test_valid_email_with_mx_records(self, mock_dns, mock_hunter):
        """Un email con registros MX válidos debe aceptarse."""
        mock_hunter.return_value.json.return_value = {
            "data": {"disposable": False, "smtp_check": True, "mx_records": True, "score": 90, "status": "valid"}
        }
        mock_dns.return_value = [MagicMock()]  # Simula una respuesta MX válida

        email = "test@realcompany.com"
        result = email_is_legitimate(email)
        self.assertTrue(result)

    @patch("user_app.adapters.requests.get")
    def test_email_already_blocked_in_db(self, mock_hunter):
        """If an email is already in the blocked database, it should be rejected without a call to Hunter."""
        BlockedEmailDomain.objects.create(username="test", domain="baddomain")

        email = "test@baddomain.com"
        result = email_is_legitimate(email)
        self.assertFalse(result)
        mock_hunter.assert_not_called()

    @patch("user_app.adapters.requests.get")
    def test_block_email_with_long_extension(self, mock_hunter):
        """Verify that emails with multi-level domains are blocked."""
        mock_hunter.return_value.json.return_value = {
            "data": {"disposable": True, "smtp_check": False, "mx_records": False, "score": 10, "status": "invalid"}
        }

        email = "spam@malicious.gov.uk"
        result = email_is_legitimate(email)
        self.assertFalse(result)
        self.assertTrue(BlockedEmailDomain.objects.filter(domain="malicious").exists())
        self.assertTrue(BlockedEmailDomainExtension.objects.filter(domain_extension="gov.uk").exists())

    @patch("user_app.adapters.requests.get", side_effect=requests.exceptions.RequestException)
    def test_hunter_api_failure(self, mock_hunter):
        """Si la API de Hunter falla, el email debe ser rechazado automáticamente."""
        email = "unknown@random.com"
        result = email_is_legitimate(email)
        self.assertFalse(result)
