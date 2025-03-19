# `qa_templates.py` Documentation

This document provides an overview of the `qa_templates.py` file, which contains a base class for Django test cases with
additional features to facilitate testing. The base class, `BaseTestCase`, extends Django's `TestCase` and includes
various utility methods for making HTTP requests, asserting response codes, managing user authentication, and more.

## Classes

### `BaseTestCase`

A Django `TestCase` with additional features for making HTTP requests, asserting response codes, managing user
authentication, and more.

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
- `_assert_response_code(status_code, response=None, msg=None)`: Asserts that the response has the specified status
  code.
- `response_200(response=None, msg=None)`: Asserts that the response has status code 200.
- `response_201(response=None, msg=None)`: Asserts that the response has status code 201.
- `response_204(response=None, msg=None)`: Asserts that the response has status code 204.
- `response_400(response=None, msg=None)`: Asserts that the response has status code 400.
- `response_403(response=None, msg=None)`: Asserts that the response has status code 403.
- `response_404(response=None, msg=None)`: Asserts that the response has status code 404.
- `response_code(response=None, status_code=None, msg=None)`: Asserts that the response has the specified status code.
- `response_code_in_range(response=None, msg=None, start=200, end=299)`: Asserts that the response status code is within
  the specified range.
- `assert_login_required(url, *args, **kwargs)`: Asserts that login is required to access the specified URL.
- `login(*args, **credentials)`: Logs in a user.
- `logout()`: Logs out a user.
- `reverse(name, *args, **kwargs)`: Reverses a URL name to a URL.
- `make_user(username=None, password=None, email=None, perms=None)`: Creates a user with the specified attributes.
- `assert_num_queries_less_than(num, *args, **kwargs)`: Asserts that the number of executed queries is less than the
  specified number.
- `assert_good_view(url_name, *args, verbose=False, **kwargs)`: Asserts that the view is good by making a GET request
  and checking the response.
- `assert_response_contains(text, response=None, html=True, **kwargs)`: Asserts that the response contains the specified
  text.
- `assert_response_not_contains(text, response=None, html=True, **kwargs)`: Asserts that the response does not contain
  the specified text.
- `assert_response_headers(headers, response=None)`: Asserts that the response contains the specified headers.
- `get_context(key)`: Returns the context value for the specified key.
- `assert_in_context(key)`: Asserts that the specified key is in the context.
- `assert_context(key, value)`: Asserts that the context value for the specified key matches the expected value.

### `ClassBaseViewTestCase`

A base class for testing class-based views with authentication.

#### Attributes

- `endpoint_name`: The name of the endpoint to test.
- `is_authenticated`: Whether the user should be authenticated.
- `kwargs`: Additional keyword arguments for the request.
- `args`: Additional arguments for the request.

#### Methods

- `setUp()`: Sets up the test case by creating a user and logging them in or out based on `is_authenticated`.
- `create_user()`: Creates a user for the test case.
- `authenticate()`: Logs in the user.
- `unauthenticate()`: Logs out the user.
- `get(*args, **kwargs)`: Makes a GET request to the endpoint.
- `post(data, *args, **kwargs)`: Makes a POST request to the endpoint.
- `put(data, *args, **kwargs)`: Makes a PUT request to the endpoint.
- `delete(*args, **kwargs)`: Makes a DELETE request to the endpoint.
- `get_check_200(url, *args, **kwargs)`: Makes a GET request and asserts that the response has status code 200.
- `assert_login_required(url, *args, **kwargs)`: Asserts that login is required to access the specified URL.

## Usage Examples

### Example 1: Testing GET Requests

```python
from blog_app.tests.view_tests.comment_view_test import CommentViewGetPostTestCase


class MyGetTestCase(CommentViewGetPostTestCase):
    def test_get_comments(self):
        response = self.get()
        self.response_code(response=response, status_code=200)
```

### Example 2: Testing POST Requests

```python
from blog_app.tests.view_tests.comment_view_test import CommentViewGetPostTestCase


class MyPostTestCase(CommentViewGetPostTestCase):
    def test_post_comment(self):
        data = {"content": "This is a good comment."}
        response = self.post(data=data)
        self.response_code(response=response, status_code=201)
```

### Example 3: Testing PUT Requests

```python
from blog_app.tests.view_tests.comment_view_test import CommentViewPutDeleteTestCase


class MyPutTestCase(CommentViewPutDeleteTestCase):
    def test_put_comment(self):
        data = {"content": "This is a very good comment."}
        response = self.put(data=data)
        self.response_code(response=response, status_code=200)
```

### Example 4: Testing DELETE Requests

```python
from blog_app.tests.view_tests.comment_view_test import CommentViewPutDeleteTestCase


class MyDeleteTestCase(CommentViewPutDeleteTestCase):
    def test_delete_comment(self):
        response = self.delete()
        self.response_code(response=response, status_code=200)
```

### Example 5: using login and logout statements.

```python
from blog_app.tests.view_tests.comment_view_test import CommentViewGetPostTestCase


class MyLoginLogoutTestCase(CommentViewGetPostTestCase):

    def test_login_get(self):
        with self.login():
            response = self.get()
            self.response_code(response=response, status_code=200)

    def test_logout_get(self):
        with self.logout():
            response = self.get()
            self.response_code(response=response, status_code=200)
```

