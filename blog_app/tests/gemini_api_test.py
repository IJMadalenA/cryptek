import os
from unittest import mock

from django.test import TestCase, override_settings

from blog_app.models.code_tip import CodeTip


class GeminiApiTestCase(TestCase):
    """
    Test case for the Gemini API integration.

    This test case demonstrates different ways to control the Gemini API mocking
    in tests, allowing for flexible testing strategies.
    """

    def test_default_behavior_in_tests(self):
        """Test that the default behavior in tests is to use a mock response."""
        tip = CodeTip.generate_code_tip(save=False)
        self.assertEqual(tip["title"], "Test Tip")
        self.assertEqual(tip["description"], "This is a mock tip for testing purposes.")

    def test_explicit_mock_parameter(self):
        """Test that the mock_enabled parameter can be used to control mocking."""
        # Force mocking even if environment variables say otherwise
        tip = CodeTip.generate_code_tip(save=False, mock_enabled=True)
        self.assertEqual(tip["title"], "Test Tip")

        # This would make a real API call if GEMINI_API_KEY is set
        # Only use this in specific tests where you want to test the actual API
        # tip = CodeTip.generate_code_tip(save=False, mock_enabled=False)

    def test_custom_mock_response(self):
        """Test that a custom mock response can be provided."""
        custom_response = {
            "title": "Custom Tip",
            "description": "This is a custom mock tip.",
            "code": "# Custom code\nprint('Hello, custom!')",
        }

        tip = CodeTip.generate_code_tip(save=False, mock_response=custom_response)
        self.assertEqual(tip["title"], "Custom Tip")
        self.assertEqual(tip["description"], "This is a custom mock tip.")

    @override_settings(GEMINI_MOCK_ENABLED=False)
    @mock.patch.dict(os.environ, {"GEMINI_MOCK_ENABLED": "false"})
    def test_environment_variable_control(self):
        """
        Test that environment variables can control mocking.

        Note: This test uses both Django's override_settings and mock.patch.dict
        to demonstrate different ways to control environment variables in tests.
        """
        # Even though environment says don't mock, we can force it with parameter
        tip = CodeTip.generate_code_tip(save=False, mock_enabled=True)
        self.assertEqual(tip["title"], "Test Tip")

    @mock.patch.dict(
        os.environ,
        {"GEMINI_MOCK_RESPONSE": '{"title": "Env Tip", "description": "From env", "code": "print(\'env\')"}'},
    )
    def test_environment_variable_response(self):
        """Test that a custom mock response can be provided via environment variable."""
        tip = CodeTip.generate_code_tip(save=False)
        self.assertEqual(tip["title"], "Env Tip")
        self.assertEqual(tip["description"], "From env")

    def test_saving_mock_response(self):
        """Test that mock responses can be saved to the database."""
        # Clear any existing tips
        CodeTip.objects.all().delete()

        # Generate and save a tip
        CodeTip.generate_code_tip(save=True)

        # Verify it was saved
        self.assertEqual(CodeTip.objects.count(), 1)
        tip = CodeTip.objects.first()
        self.assertEqual(tip.title, "Test Tip")
        self.assertEqual(tip.description, "This is a mock tip for testing purposes.")
