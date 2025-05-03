# Django Testing Framework Documentation

This documentation provides a comprehensive guide to the Django testing framework in the `qa_templates.py` file. This framework extends Django's built-in testing capabilities with additional features to make testing Django views and APIs easier and more efficient.

## Overview

The testing framework includes several classes that provide a wide range of testing utilities:

- `BaseTestCase`: A base class with general testing utilities
- `ClassBaseViewTestCase`: A specialized class for testing Django class-based views
- `StatusCodeAssertionMixin`: A mixin that provides HTTP status code assertions

These classes provide a comprehensive set of tools for testing various aspects of Django applications, including:

- **Authentication support**: Easy setup for authenticated and unauthenticated tests
- **HTTP method support**: Methods for GET, POST, PUT, PATCH, DELETE requests
- **JSON request/response support**: Methods for sending and validating JSON data
- **File upload support**: Support for testing file uploads with multipart forms
- **Query parameter support**: Easy addition of query parameters to requests
- **Custom header support**: Easy addition of custom headers to requests
- **Form testing support**: Methods for validating form submissions and errors
- **API testing support**: Methods for testing API responses
- **Permissions testing support**: Methods for testing permission requirements
- **Pagination testing support**: Methods for testing paginated responses

## Basic Usage

To use the `ClassBaseViewTestCase`, follow these steps:

1. Create a test class that inherits from `ClassBaseViewTestCase`
2. Set the `endpoint_name` attribute to the name of the URL pattern to test
3. Set the `is_authenticated` attribute to `True` or `False`
4. Optionally set the `kwargs` and `args` attributes for URL parameters
5. Implement test methods

```python
from cryptek.qa_templates import ClassBaseViewTestCase

class MyViewTestCase(ClassBaseViewTestCase):
    endpoint_name = 'my_app:my_view'
    is_authenticated = True
    kwargs = {'slug': 'my-slug'}

    def test_get(self):
        response = self.get()
        self.assert_http_200_ok(response)
        self.assertTemplateUsed(response, 'my_template.html')
```

## Authentication

The `ClassBaseViewTestCase` handles authentication automatically based on the `is_authenticated` attribute. You can also use the `authenticate` and `unauthenticate` methods to change the authentication state during a test:

```python
def test_authentication(self):
    # Start authenticated (based on is_authenticated = True)
    response = self.get()
    self.assert_http_200_ok(response)

    # Log out
    self.unauthenticate()
    response = self.get()
    self.assert_http_302_found(response)  # Redirects to login page

    # Log back in
    self.authenticate()
    response = self.get()
    self.assert_http_200_ok(response)
```

## HTTP Methods

The `ClassBaseViewTestCase` provides methods for all common HTTP methods:

```python
def test_http_methods(self):
    # GET request
    response = self.get()
    self.assert_http_200_ok(response)

    # POST request
    response = self.post(data={'name': 'Test'})
    self.assert_http_201_created(response)

    # PUT request
    response = self.put(data={'name': 'Updated Test'})
    self.assert_http_200_ok(response)

    # PATCH request
    response = self.patch(data={'name': 'Partially Updated'})
    self.assert_http_200_ok(response)

    # DELETE request
    response = self.delete()
    self.assert_http_204_no_content(response)
```

## Query Parameters and Headers

You can add query parameters and custom headers to requests:

```python
def test_query_params_and_headers(self):
    # With query parameters
    response = self.get(query_params={'page': 1, 'sort': 'name'})
    self.assert_http_200_ok(response)

    # With custom headers
    response = self.get(headers={'Accept': 'application/json'})
    self.assert_http_200_ok(response)

    # With both
    response = self.get(
        query_params={'page': 1},
        headers={'Accept': 'application/json'}
    )
    self.assert_http_200_ok(response)
```

## JSON Requests and Responses

You can send and validate JSON data:

```python
def test_json(self):
    # Send JSON data
    data = {'name': 'Test', 'description': 'This is a test'}
    response = self.post(data=data, format='json')

    # Validate JSON response
    data = self.assert_json_response(response, status_code=201)
    self.assertEqual(data['name'], 'Test')
```

## Form Testing

You can test form submissions and validation:

```python
def test_form(self):
    # Valid form
    data = {'name': 'Test', 'email': 'test@example.com'}
    response = self.post(data=data)
    self.assert_http_302_found(response)  # Redirects after successful submission

    # Invalid form
    data = {'name': '', 'email': 'invalid-email'}
    response = self.post(data=data)
    self.assert_http_200_ok(response)  # Re-renders form with errors
    self.assert_form_error(response, 'form', 'name', 'This field is required.')
    self.assert_form_error(response, 'form', 'email', 'Enter a valid email address.')
```

## Permissions Testing

You can test permission requirements:

```python
def test_permissions(self):
    # Test that a specific permission is required
    self.assert_permission_required('my_app.change_mymodel')
```

## Pagination Testing

You can test paginated responses:

```python
def test_pagination(self):
    response = self.get(query_params={'page': 1})
    self.assert_http_200_ok(response)
    self.assert_pagination(response, expected_count=20, page_size=10)
```

## Class Reference

### `BaseTestCase`

A Django `TestCase` with additional features for making HTTP requests, asserting response codes, managing user authentication, and more.

#### Attributes

- `user_factory`: A factory for creating user instances.
- `last_response`: The last HTTP response received.

#### Methods

- `_request(method_name, url_name, *args, **kwargs)`: Makes an HTTP request using the specified method and URL name.
- `get(url_name, *args, **kwargs)`: Makes a GET request.
- `post(url_name, *args, **kwargs)`: Makes a POST request.
- `put(url_name, *args, **kwargs)`: Makes a PUT request.
- `patch(url_name, *args, **kwargs)`: Makes a PATCH request.
- `head(url_name, *args, **kwargs)`: Makes a HEAD request.
- `options(url_name, *args, **kwargs)`: Makes an OPTIONS request.
- `delete(url_name, *args, **kwargs)`: Makes a DELETE request.
- `_which_response(response=None)`: Returns the last response if no response is provided.
- `_assert_response_code(status_code, response=None, msg=None)`: Asserts that the response has the specified status code.
- `response_200(response=None, msg=None)`: Asserts that the response has status code 200.
- `response_201(response=None, msg=None)`: Asserts that the response has status code 201.
- `response_204(response=None, msg=None)`: Asserts that the response has status code 204.
- `response_400(response=None, msg=None)`: Asserts that the response has status code 400.
- `response_403(response=None, msg=None)`: Asserts that the response has status code 403.
- `response_404(response=None, msg=None)`: Asserts that the response has status code 404.
- `response_code(response=None, status_code=None, msg=None)`: Asserts that the response has the specified status code.
- `response_code_in_range(response=None, msg=None, start=200, end=299)`: Asserts that the response status code is within the specified range.
- `assert_login_required(url, *args, **kwargs)`: Asserts that login is required to access the specified URL.
- `login(*args, **credentials)`: Logs in a user.
- `logout()`: Logs out a user.
- `reverse(name, *args, **kwargs)`: Reverses a URL name to a URL.
- `make_user(username=None, password=None, email=None, perms=None)`: Creates a user with the specified attributes.
- `assert_num_queries_less_than(num, *args, **kwargs)`: Asserts that the number of executed queries is less than the specified number.
- `assert_good_view(url_name, *args, verbose=False, **kwargs)`: Asserts that the view is good by making a GET request and checking the response.
- `assert_response_contains(text, response=None, html=True, **kwargs)`: Asserts that the response contains the specified text.
- `assert_response_not_contains(text, response=None, html=True, **kwargs)`: Asserts that the response does not contain the specified text.
- `assert_response_headers(headers, response=None)`: Asserts that the response contains the specified headers.
- `get_context(key)`: Returns the context value for the specified key.
- `assert_in_context(key)`: Asserts that the specified key is in the context.
- `assert_context(key, value)`: Asserts that the context value for the specified key matches the expected value.

### `ClassBaseViewTestCase`

A base class for testing class-based views with authentication. This class inherits from both `TestCase` and `BaseTestCase`.

#### Attributes

- `endpoint_name`: The name of the endpoint to test.
- `is_authenticated`: Whether the user should be authenticated.
- `kwargs`: Additional keyword arguments for the request.
- `args`: Additional arguments for the request.
- `user_factory`: A factory for creating user instances.
- `default_content_type`: The default content type for requests.

#### Methods

- `setUp()`: Sets up the test case by creating a user and logging them in or out based on `is_authenticated`.
- `create_user(username="test_user", password="test_password", **kwargs)`: Creates a user for the test case.
- `authenticate(user=None, password=None)`: Logs in the user.
- `unauthenticate()`: Logs out the user.
- `get_url(endpoint_name=None, args=None, kwargs=None)`: Gets the URL for the specified endpoint.
- `get(query_params=None, headers=None, *args, **kwargs)`: Makes a GET request to the endpoint.
- `post(data=None, format='form', query_params=None, headers=None, *args, **kwargs)`: Makes a POST request to the endpoint.
- `put(data=None, format='form', query_params=None, headers=None, *args, **kwargs)`: Makes a PUT request to the endpoint.
- `patch(data=None, format='form', query_params=None, headers=None, *args, **kwargs)`: Makes a PATCH request to the endpoint.
- `delete(query_params=None, headers=None, *args, **kwargs)`: Makes a DELETE request to the endpoint.
- `get_check_200(url=None, *args, **kwargs)`: Makes a GET request and asserts that the response has status code 200.
- `assert_login_required(url=None, *args, **kwargs)`: Asserts that login is required to access the specified URL.
- `assert_permission_required(permission, url=None, *args, **kwargs)`: Asserts that the specified permission is required to access the URL.
- `assert_json_response(response, expected_data=None, status_code=200)`: Asserts that the response contains valid JSON and optionally checks its content.
- `assert_form_error(response, form_name, field_name, error_msg=None)`: Asserts that the response contains a form error.
- `assert_pagination(response, page_obj_name='page_obj', expected_count=None, page_size=None)`: Asserts that the response contains paginated results.

### `StatusCodeAssertionMixin`

A mixin that provides HTTP status code assertions.

#### Methods

- `_assert_http_status(status_code, response=None, msg=None, url=None)`: Asserts that the response has the specified status code.
- `assert_http_200_ok(response=None, msg=None)`: Asserts that the response has status code 200.
- `assert_http_201_created(response=None, msg=None)`: Asserts that the response has status code 201.
- `assert_http_204_no_content(response=None, msg=None)`: Asserts that the response has status code 204.
- `assert_http_400_bad_request(response=None, msg=None)`: Asserts that the response has status code 400.
- `assert_http_403_forbidden(response=None, msg=None)`: Asserts that the response has status code 403.
- `assert_http_404_not_found(response=None, msg=None)`: Asserts that the response has status code 404.
- And many more for other HTTP status codes.

## Additional Usage Examples

### Using Login and Logout Context Managers

You can use the `login` and `logout` context managers to temporarily change the authentication state:

```python
from cryptek.qa_templates import ClassBaseViewTestCase

class MyLoginLogoutTestCase(ClassBaseViewTestCase):
    endpoint_name = 'my_app:my_view'
    is_authenticated = True  # Default state is authenticated

    def test_login_get(self):
        with self.login():  # Explicitly login (already logged in, but demonstrates the context manager)
            response = self.get()
            self.response_code(response=response, status_code=200)

    def test_logout_get(self):
        with self.logout():  # Temporarily logout
            response = self.get()
            self.response_code(response=response, status_code=302)  # Redirects to login page
```

### Testing Comments API

Here's an example of testing a comments API:

```python
from cryptek.qa_templates import ClassBaseViewTestCase

class CommentViewTestCase(ClassBaseViewTestCase):
    endpoint_name = 'api:comments'
    is_authenticated = True

    def setUp(self):
        # Create a test entry and comments
        self.entry = EntryFactory.create(status=1)
        CommentFactory.create_batch(3, entry=self.entry)
        self.kwargs = {"slug": self.entry.slug}
        super().setUp()

    def test_get_comments(self):
        response = self.get()
        self.response_code(response=response, status_code=200)
        response_data = json.loads(response.content)
        self.assertIn("comments", response_data)
        self.assertTrue(len(response_data["comments"]) > 0)

    def test_post_comment(self):
        data = {"content": "This is a test comment."}
        response = self.post(data=data)
        self.response_code(response=response, status_code=201)
        response_data = json.loads(response.content)
        self.assertIn("message", response_data)

    def test_put_comment(self):
        # First create a comment
        comment = CommentFactory.create(user=self.user_instance)
        self.kwargs = {"slug": comment.entry.slug, "pk": comment.id}

        # Then update it
        data = {"content": "This is an updated comment."}
        response = self.put(data=data)
        self.response_code(response=response, status_code=200)

    def test_delete_comment(self):
        # First create a comment
        comment = CommentFactory.create(user=self.user_instance)
        self.kwargs = {"slug": comment.entry.slug, "pk": comment.id}

        # Then delete it
        response = self.delete()
        self.response_code(response=response, status_code=200)
```

## Complete Example

For a complete example of how to use the `ClassBaseViewTestCase`, see the `qa_templates_example.py` file, which includes examples for testing list views, form views, and API views.

## Best Practices

1. **Use descriptive test method names**: Name your test methods to clearly describe what they're testing.
2. **Test one thing per method**: Each test method should test a specific aspect of the view.
3. **Use the assertion methods**: Use the provided assertion methods (`assert_http_200_ok`, `assert_json_response`, etc.) instead of direct assertions when possible.
4. **Set up test data in setUp**: Create any necessary test data in the `setUp` method.
5. **Clean up after tests**: Use `tearDown` to clean up any resources created during tests.
6. **Use factories**: Use factory libraries like `factory_boy` to create test data.
7. **Mock external services**: Use `unittest.mock` to mock external services.
8. **Test edge cases**: Test edge cases like empty data, invalid data, and error conditions.
9. **Test permissions**: Test that views enforce the correct permissions.
10. **Test with different users**: Test with different types of users (anonymous, regular, staff, superuser).
