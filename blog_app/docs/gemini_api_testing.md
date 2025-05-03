# Gemini API Testing Guide

This document explains how to test code that interacts with the Gemini API in the Cryptek project.

## Overview

The `CodeTip` model provides a flexible way to mock the Gemini API during tests. This allows you to:

1. Test code that uses the Gemini API without making actual API calls
2. Verify that the API is called correctly when needed
3. Test how your code handles different API responses
4. Make real API calls in specific tests when necessary

## Mocking Options

There are several ways to control whether the Gemini API is mocked:

### 1. Default Behavior

By default, when running tests (when 'test' is in `sys.argv`), the Gemini API calls are automatically mocked with a default response:

```python
tip = CodeTip.generate_code_tip()
# Uses a mock response, no real API call is made
```

### 2. Explicit Parameters

You can explicitly control mocking using parameters:

```python
# Force mocking even outside of tests
tip = CodeTip.generate_code_tip(mock_enabled=True)

# Force real API call even in tests (use sparingly)
tip = CodeTip.generate_code_tip(mock_enabled=False)
```

### 3. Environment Variables

You can control mocking using environment variables:

```python
# In your .env file or environment
GEMINI_MOCK_ENABLED=true  # or false
```

Or in tests:

```python
from unittest import mock
import os

@mock.patch.dict(os.environ, {"GEMINI_MOCK_ENABLED": "false"})
def test_something():
    # Will use real API unless overridden by parameter
    tip = CodeTip.generate_code_tip()
```

## Custom Mock Responses

You can provide custom mock responses in several ways:

### 1. Via Parameter

```python
custom_response = {
    "title": "Custom Tip",
    "description": "This is a custom mock tip.",
    "code": "# Custom code\nprint('Hello, custom!')",
}

tip = CodeTip.generate_code_tip(mock_response=custom_response)
```

### 2. Via Environment Variable

```python
# In your .env file or environment
GEMINI_MOCK_RESPONSE='{"title": "Env Tip", "description": "From env", "code": "print(\'env\')"}'
```

Or in tests:

```python
@mock.patch.dict(os.environ, {
    "GEMINI_MOCK_RESPONSE": '{"title": "Env Tip", "description": "From env", "code": "print(\'env\')"}'
})
def test_something():
    tip = CodeTip.generate_code_tip()
    # Will use the mock response from the environment variable
```

## Testing Database Interactions

You can test that tips are correctly saved to the database:

```python
def test_saving_tip():
    # Clear any existing tips
    CodeTip.objects.all().delete()
    
    # Generate and save a tip
    CodeTip.generate_code_tip(save=True)
    
    # Verify it was saved
    assert CodeTip.objects.count() == 1
    tip = CodeTip.objects.first()
    assert tip.title == "Test Tip"
```

## Testing Real API Calls

In some cases, you may want to test the actual API integration. Use this sparingly, as it depends on external services and may incur costs:

```python
def test_real_api_call():
    # Only run this test if GEMINI_API_KEY is set
    if not os.environ.get("GEMINI_API_KEY"):
        self.skipTest("GEMINI_API_KEY not set")
    
    # Make a real API call
    tip = CodeTip.generate_code_tip(mock_enabled=False)
    
    # Verify the response
    assert "title" in tip
    assert "description" in tip
    assert "code" in tip
```

## Best Practices

1. **Default to mocking**: Most tests should use mocked responses to avoid external dependencies.
2. **Test edge cases**: Use custom mock responses to test how your code handles different API responses.
3. **Test error handling**: Provide mock responses that simulate API errors to test your error handling.
4. **Limit real API calls**: Only make real API calls in specific tests that verify the API integration.
5. **Use environment variables**: Use environment variables to control mocking in CI/CD pipelines.

## Example Test Class

See `blog_app/tests/gemini_api_test.py` for a complete example of how to test code that interacts with the Gemini API.