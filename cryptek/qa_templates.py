import secrets

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models import Q
from django.shortcuts import resolve_url
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import NoReverseMatch, reverse
from factory.fuzzy import FuzzyText

from cryptek.status_code_assertion import StatusCodeAssertionMixin

if hasattr(TestCase, "assertURLEqual"):
    assertURLEqual = TestCase.assertURLEqual
else:

    def assert_url_equal(t, url1, url2, msg_prefix=""):
        raise NotImplementedError("Your version of Django does not support `assertURLEqual`")


class _AssertNumQueriesLessThanContext(CaptureQueriesContext):
    """
    Context manager to assert that the number of executed queries is less than a specified number.

    Attributes:
        test_case (DjangoTestCase): The test case instance.
        num (int): The maximum number of queries allowed.
        verbose (bool): If True, prints the executed queries if the assertion fails.
    """

    def __init__(self, test_case, num, connection, verbose=False):
        self.test_case = test_case
        self.num = num
        self.verbose = verbose
        super(_AssertNumQueriesLessThanContext, self).__init__(connection)

    def __exit__(self, exc_type, exc_value, traceback):
        super(_AssertNumQueriesLessThanContext, self).__exit__(exc_type, exc_value, traceback)
        if exc_type is not None:
            return
        executed = len(self)
        msg = "%d queries executed, expected less than %d" % (executed, self.num)
        if self.verbose:
            queries = "\n\n".join(q["sql"] for q in self.captured_queries)
            msg += ". Executed queries were:\n\n%s" % queries
        self.test_case.assertLess(executed, self.num, msg)


class _GenericContext:
    def __init__(self, testcase, *args, **credentials):
        self.testcase = testcase
        self.credentials = credentials
        self.user = get_user_model()
        self.password = secrets.token_urlsafe(16)

        if args and isinstance(args[0], self.user):
            """
            If the first argument is an instance of the user model, we will use it to create the user.
            This is useful for testing views that require a user to be logged in.
            """
            self.user_instance = args[0]
            self.user_instance.set_password(self.credentials.get("password", self.password))
            self.user_instance.save()
            self.credentials.update(
                {
                    "username": getattr(self.user_instance, "username"),
                    "password": self.credentials.get("password", self.password),
                }
            )
        else:
            """
            If the first argument is not an instance of the user model, we will create a new user.
            """
            self.user_instance = self.user.objects.create_user(
                username=self.credentials.get("username", "username"),
                password=self.credentials.get("password", self.password),
            )
            self.credentials.update(
                {
                    "username": self.user_instance.username,
                    "password": self.credentials.get("password", self.password),
                }
            )

    def login(self):
        success = self.testcase.client.login(**self.credentials)
        self.testcase.assertTrue(success, "login failed with credentials=%r" % self.credentials)

    def logout(self):
        self.testcase.client.logout()


class _AuthenticatedContext(_GenericContext):
    def __enter__(self):
        self.login()

    def __exit__(self, *args):
        self.logout()


class _UnauthenticatedContext(_GenericContext):
    def __enter__(self):
        self.logout()

    def __exit__(self, *args):
        self.login()


class BaseTestCase(StatusCodeAssertionMixin):
    """
    Django TestCase with helpful additional features
    """

    user_factory = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.last_response = None

    def _request(self, method_name, url_name, *args, **kwargs):
        """
        Request url by name using reverse() through method

        If reverse raises NoReverseMatch attempt to use it as a URL.
        """
        follow = kwargs.pop("follow", False)
        extra = kwargs.pop("extra", {})
        data = kwargs.pop("data", {})

        valid_method_names = [
            "get",
            "post",
            "put",
            "patch",
            "head",
            "trace",
            "options",
            "delete",
        ]

        if method_name in valid_method_names:
            method = getattr(self.client, method_name)
        else:
            raise LookupError("Cannot find the method {0}".format(method_name))

        try:
            self.last_response = method(
                reverse(url_name, args=args, kwargs=kwargs),
                data=data,
                follow=follow,
                **extra,
            )
        except NoReverseMatch:
            self.last_response = method(url_name, data=data, follow=follow, **extra)

        self.context = self.last_response.context
        return self.last_response

    def get(self, url_name, *args, **kwargs):
        return self._request("get", url_name, *args, **kwargs)

    def post(self, url_name, *args, **kwargs):
        return self._request("post", url_name, *args, **kwargs)

    def put(self, url_name, *args, **kwargs):
        return self._request("put", url_name, *args, **kwargs)

    def patch(self, url_name, *args, **kwargs):
        return self._request("patch", url_name, *args, **kwargs)

    def head(self, url_name, *args, **kwargs):
        return self._request("head", url_name, *args, **kwargs)

    def options(self, url_name, *args, **kwargs):
        return self._request("options", url_name, *args, **kwargs)

    def delete(self, url_name, *args, **kwargs):
        return self._request("delete", url_name, *args, **kwargs)

    def _which_response(self, response=None):
        if response is None and self.last_response is not None:
            return self.last_response
        else:
            return response

    def _assert_response_code(self, status_code, response=None, msg=None):
        response = self._which_response(response)
        self.assertTrue(response)
        self.assertEqual(status_code, response.status_code, msg)

    def response_200(self, response=None, msg=None):
        """Given response has status_code 200"""
        self._assert_response_code(200, response, msg)

    def response_201(self, response=None, msg=None):
        """Given response has status_code 201"""
        self._assert_response_code(201, response, msg)

    def response_204(self, response=None, msg=None):
        """Given response has status_code 204"""
        self._assert_response_code(204, response, msg)

    def response_400(self, response=None, msg=None):
        """Given response has status_code 400"""
        self._assert_response_code(400, response, msg)

    def response_403(self, response=None, msg=None):
        """Given response has status_code 403"""
        self._assert_response_code(403, response, msg)

    def response_404(self, response=None, msg=None):
        """Given response has status_code 404"""
        self._assert_response_code(404, response, msg)

    def response_code(self, response=None, status_code: int = None, msg=None):
        response = self._which_response(response)
        self.assertTrue(response)
        self.assertEqual(status_code, response.status_code, msg)

    def response_code_in_range(self, response=None, msg=None, start=200, end=299):
        response = self._which_response(response)
        self.assertTrue(start <= response.status_code <= end, msg)

    def assert_login_required(self, url, *args, **kwargs):
        response = self.get(url, *args, **kwargs)
        reversed_url = reverse(url, args=args, kwargs=kwargs)
        login_url = str(resolve_url(settings.LOGIN_URL))
        expected_url = "{0}?next={1}".format(login_url, reversed_url)
        self.assertRedirects(response, expected_url)

    assertRedirects = TestCase.assertRedirects

    def login(self, *args, **credentials):
        """Login a user"""
        return _AuthenticatedContext(self, *args, **credentials)

    def logout(self):
        """Logout a user"""
        return _UnauthenticatedContext(self)

    @staticmethod
    def reverse(name, *args, **kwargs):
        """Reverse a url, convenience to avoid having to import reverse in tests"""
        return reverse(name, args=args, kwargs=kwargs)

    @classmethod
    def make_user(
        cls,
        username=None,
        password=None,
        email=None,
        perms=None,
    ):
        if username is None:
            username = f"username_{FuzzyText(length=8).fuzz()}"
        if password is None:
            password = FuzzyText(length=12).fuzz()
        if email is None:
            email = f"{FuzzyText(length=8).fuzz()}@test.com"

        user = get_user_model().objects.create_user(
            username=str(username),
            password=password,
            email=str(email),
        )

        if perms:
            from django.contrib.auth.models import Permission

            _filter = Q()
            for perm in perms:
                if "." not in perm:
                    raise ImproperlyConfigured(
                        "The permission in the perms argument needs to be either "
                        "app_label.codename or app_label.* (e.g. accounts.change_user or accounts.*)"
                    )
                app_label, codename = perm.split(".")
                if codename == "*":
                    _filter = _filter | Q(content_type__app_label=app_label)
                else:
                    _filter = _filter | Q(content_type__app_label=app_label, codename=codename)
            user.user_permissions.add(*list(Permission.objects.filter(_filter)))

        return {
            "user": user,
            "username": username,
            "password": password,
            "email": email,
        }

    def assert_num_queries_less_than(self, num, *args, **kwargs):
        func = kwargs.pop("func", None)
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        verbose = kwargs.pop("verbose", False)
        conn = connections[using]

        context = _AssertNumQueriesLessThanContext(self, num, conn, verbose=verbose)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)

    def assert_good_view(self, url_name, *args, verbose=False, **kwargs):
        query_count = kwargs.pop("test_query_count", 50)

        with self.assert_num_queries_less_than(query_count, verbose=verbose):
            response = self.get(url_name, *args, **kwargs)

        self.response_200(response)

        return response

    def assert_response_contains(self, text, response=None, html=True, **kwargs):
        response = self._which_response(response)
        self.assertContains(response, text, html=html, **kwargs)

    def assert_response_not_contains(self, text, response=None, html=True, **kwargs):
        response = self._which_response(response)
        self.assertNotContains(response, text, html=html, **kwargs)

    def assert_response_headers(self, headers, response=None):
        response = self._which_response(response)
        compare = {h: response.get(h) for h in headers}
        self.assertEqual(compare, headers)

    def get_context(self, key):
        if self.last_response is not None:
            self.assertIn(key, self.last_response.context)
            return self.last_response.context[key]
        else:
            raise Exception("There isn't a previous response to query")

    def assert_in_context(self, key):
        return self.get_context(key)

    def assert_context(self, key, value):
        self.assertEqual(self.get_context(key), value)


class ClassBaseViewTestCase(TestCase, BaseTestCase):
    """
    Base class for testing class-based views with authentication.

    This class provides a comprehensive set of tools for testing Django views, including:
    - Authentication support (login/logout)
    - HTTP method support (GET, POST, PUT, PATCH, DELETE)
    - JSON request/response support
    - File upload support
    - Query parameter support
    - Custom header support
    - Form testing support
    - API testing support
    - Permissions testing support
    - Pagination testing support

    Usage:
    1. Subclass this class
    2. Set the endpoint_name attribute to the name of the URL pattern to test
    3. Set the is_authenticated attribute to True or False
    4. Optionally set the kwargs and args attributes for URL parameters
    5. Implement test methods

    Example:
    ```python
    class MyViewTestCase(ClassBaseViewTestCase):
        endpoint_name = 'my_app:my_view'
        is_authenticated = True
        kwargs = {'slug': 'my-slug'}

        def test_get(self):
            response = self.get()
            self.assert_http_200_ok(response)
            self.assertTemplateUsed(response, 'my_template.html')
    ```
    """

    endpoint_name = None
    is_authenticated = None
    kwargs = None
    args = None
    user_factory = None
    default_content_type = "application/x-www-form-urlencoded"

    def setUp(self):
        """
        Set up the test case.

        This method:
        1. Creates a test client
        2. Creates a test user (or uses a factory if provided)
        3. Handles authentication based on the is_authenticated attribute
        """
        self.client = Client()
        self._password = secrets.token_urlsafe(16)

        # Create user using factory if provided, otherwise use create_user method
        if self.user_factory is not None:
            self.user_instance = self.user_factory()
            self.user_instance.set_password(self._password)
            self.user_instance.save()
        else:
            self.user_instance = self.create_user()
            self.user_instance.set_password(self._password)
            self.user_instance.save()

        # Handle authentication
        if not isinstance(self.is_authenticated, bool):
            raise ValueError("is_authenticated must be set and be a boolean.")

        if self.is_authenticated:
            login_success = self.client.login(
                username=self.user_instance.username,
                password=self._password,
            )
            self.assertTrue(
                login_success,
                msg=f"Login failed - {self.user_instance.username} - {self._password}",
            )
        else:
            self.client.logout()

    @staticmethod
    def create_user(username="test_user", password="test_password", **kwargs):
        """
        Create a test user.

        Args:
            username (str): The username for the test user
            password (str): The password for the test user
            **kwargs: Additional fields to set on the user

        Returns:
            User: The created user instance
        """
        user = get_user_model().objects.create_user(username=username, password=password, **kwargs)
        return user

    def authenticate(self, user=None, password=None):
        """
        Authenticate as the specified user or the default test user.

        Args:
            user (User, optional): The user to authenticate as. Defaults to self.user_instance.
            password (str, optional): The password to use. Defaults to self._password.
        """
        user = user or self.user_instance
        password = password or self._password
        return self.client.login(username=user.username, password=password)

    def unauthenticate(self):
        """Log out the current user."""
        return self.client.logout()

    def get_url(self, endpoint_name=None, args=None, kwargs=None):
        """
        Get the URL for the specified endpoint.

        Args:
            endpoint_name (str, optional): The name of the URL pattern. Defaults to self.endpoint_name.
            args (list, optional): Positional arguments for the URL. Defaults to self.args.
            kwargs (dict, optional): Keyword arguments for the URL. Defaults to self.kwargs.

        Returns:
            str: The URL
        """
        endpoint_name = endpoint_name or self.endpoint_name
        args = args or self.args
        kwargs = kwargs or self.kwargs

        if not endpoint_name:
            raise ValueError("endpoint_name must be provided")

        return reverse(endpoint_name, args=args, kwargs=kwargs)

    def get(self, query_params=None, headers=None, *args, **kwargs):
        """
        Make a GET request to the endpoint.

        Args:
            query_params (dict, optional): Query parameters to add to the URL
            headers (dict, optional): Custom headers to add to the request
            *args, **kwargs: Additional arguments to pass to the client.get method

        Returns:
            Response: The HTTP response
        """
        url = self.get_url()

        # Add query parameters if provided
        if query_params:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

        # Add custom headers if provided
        if headers:
            kwargs.setdefault("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
            for header, value in headers.items():
                header_key = f"HTTP_{header.replace('-', '_').upper()}"
                kwargs[header_key] = value

        return self.client.get(path=url, *args, **kwargs)

    def post(self, data=None, format="form", query_params=None, headers=None, *args, **kwargs):
        """
        Make a POST request to the endpoint.

        Args:
            data (dict, optional): Data to send in the request body
            format (str, optional): Format of the data ('form', 'json', 'multipart'). Defaults to 'form'.
            query_params (dict, optional): Query parameters to add to the URL
            headers (dict, optional): Custom headers to add to the request
            *args, **kwargs: Additional arguments to pass to the client.post method

        Returns:
            Response: The HTTP response
        """
        url = self.get_url()

        # Add query parameters if provided
        if query_params:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

        # Handle different data formats
        if format == "json" and data is not None:
            import json

            kwargs["content_type"] = "application/json"
            data = json.dumps(data)
        elif format == "multipart":
            kwargs["content_type"] = None  # Let Django set the correct multipart content type
        else:  # Default to form data
            kwargs.setdefault("content_type", self.default_content_type)

        # Add custom headers if provided
        if headers:
            kwargs.setdefault("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
            for header, value in headers.items():
                header_key = f"HTTP_{header.replace('-', '_').upper()}"
                kwargs[header_key] = value

        return self.client.post(path=url, data=data, *args, **kwargs)

    def put(self, data=None, format="form", query_params=None, headers=None, *args, **kwargs):
        """
        Make a PUT request to the endpoint.

        Args:
            data (dict, optional): Data to send in the request body
            format (str, optional): Format of the data ('form', 'json', 'multipart'). Defaults to 'form'.
            query_params (dict, optional): Query parameters to add to the URL
            headers (dict, optional): Custom headers to add to the request
            *args, **kwargs: Additional arguments to pass to the client.put method

        Returns:
            Response: The HTTP response
        """
        url = self.get_url()

        # Add query parameters if provided
        if query_params:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

        # Handle different data formats
        if format == "json" and data is not None:
            import json

            kwargs["content_type"] = "application/json"
            data = json.dumps(data)
        elif format == "multipart":
            kwargs["content_type"] = None  # Let Django set the correct multipart content type
        else:  # Default to form data
            kwargs.setdefault("content_type", self.default_content_type)

        # Add custom headers if provided
        if headers:
            kwargs.setdefault("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
            for header, value in headers.items():
                header_key = f"HTTP_{header.replace('-', '_').upper()}"
                kwargs[header_key] = value

        return self.client.put(path=url, data=data, *args, **kwargs)

    def patch(self, data=None, format="form", query_params=None, headers=None, *args, **kwargs):
        """
        Make a PATCH request to the endpoint.

        Args:
            data (dict, optional): Data to send in the request body
            format (str, optional): Format of the data ('form', 'json', 'multipart'). Defaults to 'form'.
            query_params (dict, optional): Query parameters to add to the URL
            headers (dict, optional): Custom headers to add to the request
            *args, **kwargs: Additional arguments to pass to the client.patch method

        Returns:
            Response: The HTTP response
        """
        url = self.get_url()

        # Add query parameters if provided
        if query_params:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

        # Handle different data formats
        if format == "json" and data is not None:
            import json

            kwargs["content_type"] = "application/json"
            data = json.dumps(data)
        elif format == "multipart":
            kwargs["content_type"] = None  # Let Django set the correct multipart content type
        else:  # Default to form data
            kwargs.setdefault("content_type", self.default_content_type)

        # Add custom headers if provided
        if headers:
            kwargs.setdefault("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
            for header, value in headers.items():
                header_key = f"HTTP_{header.replace('-', '_').upper()}"
                kwargs[header_key] = value

        return self.client.patch(path=url, data=data, *args, **kwargs)

    def delete(self, query_params=None, headers=None, *args, **kwargs):
        """
        Make a DELETE request to the endpoint.

        Args:
            query_params (dict, optional): Query parameters to add to the URL
            headers (dict, optional): Custom headers to add to the request
            *args, **kwargs: Additional arguments to pass to the client.delete method

        Returns:
            Response: The HTTP response
        """
        url = self.get_url()

        # Add query parameters if provided
        if query_params:
            url = f"{url}?{'&'.join([f'{k}={v}' for k, v in query_params.items()])}"

        # Add custom headers if provided
        if headers:
            kwargs.setdefault("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
            for header, value in headers.items():
                header_key = f"HTTP_{header.replace('-', '_').upper()}"
                kwargs[header_key] = value

        return self.client.delete(path=url, *args, **kwargs)

    def get_check_200(self, url=None, *args, **kwargs):
        """
        Make a GET request and assert that the response has a 200 status code.

        Args:
            url (str, optional): The URL to request. Defaults to self.endpoint_name.
            *args, **kwargs: Additional arguments to pass to the get method

        Returns:
            Response: The HTTP response
        """
        if url:
            response = super(ClassBaseViewTestCase, self).get(url, *args, **kwargs)
        else:
            response = self.get(*args, **kwargs)
        self.assert_http_200_ok(response)
        return response

    def assert_login_required(self, url=None, *args, **kwargs):
        """
        Ensure login is required to access the URL.

        Args:
            url (str, optional): The URL to request. Defaults to self.endpoint_name.
            *args, **kwargs: Additional arguments to pass to the get method

        Asserts:
            That the response redirects to the login page
        """
        # Save current authentication state
        was_authenticated = self.is_authenticated

        # Force logout
        self.client.logout()

        if url:
            response = super(ClassBaseViewTestCase, self).get(url, *args, **kwargs)
            reversed_url = reverse(url, args=args, kwargs=kwargs)
        else:
            response = self.get(*args, **kwargs)
            reversed_url = self.get_url()

        login_url = str(resolve_url(settings.LOGIN_URL))
        expected_url = "{0}?next={1}".format(login_url, reversed_url)
        self.assertRedirects(response, expected_url)

        # Restore authentication state
        if was_authenticated:
            self.authenticate()

    def assert_permission_required(self, permission, url=None, *args, **kwargs):
        """
        Ensure the specified permission is required to access the URL.

        Args:
            permission (str): The permission to check (e.g., 'app_label.change_model')
            url (str, optional): The URL to request. Defaults to self.endpoint_name.
            *args, **kwargs: Additional arguments to pass to the get method

        Asserts:
            That the response has a 403 status code when the user doesn't have the permission
        """
        # Save current permissions
        original_user = self.user_instance

        # Create a new user without the permission
        no_perm_user = self.create_user(username="no_perm_user", password=self._password)
        self.client.logout()
        self.authenticate(user=no_perm_user)

        if url:
            response = super(ClassBaseViewTestCase, self).get(url, *args, **kwargs)
        else:
            response = self.get(*args, **kwargs)

        self.assert_http_403_forbidden(response)

        # Restore original user
        self.client.logout()
        self.authenticate(user=original_user)

    def assert_json_response(self, response, expected_data=None, status_code=200):
        """
        Assert that the response contains valid JSON and optionally check its content.

        Args:
            response (Response): The HTTP response
            expected_data (dict, optional): Expected data in the JSON response
            status_code (int, optional): Expected status code. Defaults to 200.

        Asserts:
            That the response has the expected status code and contains valid JSON
            If expected_data is provided, also asserts that the JSON contains the expected data
        """
        self._assert_http_status(status_code, response)

        import json

        try:
            data = json.loads(response.content.decode("utf-8"))
        except json.JSONDecodeError:
            self.fail(f"Response does not contain valid JSON: {response.content}")

        if expected_data:
            for key, value in expected_data.items():
                self.assertIn(key, data)
                self.assertEqual(data[key], value)

        return data

    def assert_form_error(self, response, form_name, field_name, error_msg=None):
        """
        Assert that the response contains a form error.

        Args:
            response (Response): The HTTP response
            form_name (str): The name of the form in the context
            field_name (str): The name of the field with the error
            error_msg (str, optional): The expected error message

        Asserts:
            That the form in the response context has an error for the specified field
            If error_msg is provided, also asserts that the error message matches
        """
        self.assertIn(form_name, response.context)
        form = response.context[form_name]
        self.assertIn(field_name, form.errors)

        if error_msg:
            self.assertIn(error_msg, form.errors[field_name])

    def assert_pagination(self, response, page_obj_name="page_obj", expected_count=None, page_size=None):
        """
        Assert that the response contains paginated results.

        Args:
            response (Response): The HTTP response
            page_obj_name (str, optional): The name of the page object in the context. Defaults to 'page_obj'.
            expected_count (int, optional): The expected total number of items
            page_size (int, optional): The expected page size

        Asserts:
            That the response context contains a page object
            If expected_count is provided, also asserts that the paginator has the expected number of items
            If page_size is provided, also asserts that the page has the expected size
        """
        self.assertIn(page_obj_name, response.context)
        page_obj = response.context[page_obj_name]

        if expected_count is not None:
            self.assertEqual(page_obj.paginator.count, expected_count)

        if page_size is not None:
            self.assertLessEqual(len(page_obj), page_size)

    def assert_content_type(self, response, content_type):
        """
        Assert that the response has the specified content type.

        Args:
            response (Response): The HTTP response
            content_type (str): The expected content type (e.g., 'application/json', 'text/html')

        Asserts:
            That the response has the expected content type
        """
        self.assertEqual(
            response["Content-Type"].split(";")[0],
            content_type,
            f"Expected content type '{content_type}', got '{response['Content-Type']}'",
        )

    def assert_response_headers(self, response, headers):
        """
        Assert that the response contains the specified headers.

        Args:
            response (Response): The HTTP response
            headers (dict): A dictionary of expected header names and values

        Asserts:
            That the response contains all the specified headers with the expected values
        """
        for header, expected_value in headers.items():
            self.assertIn(header, response, f"Expected response to contain header '{header}'")
            self.assertEqual(
                response[header],
                expected_value,
                f"Expected header '{header}' to have value '{expected_value}', got '{response[header]}'",
            )

    def assert_cors_headers(self, response, allowed_origins="*", allowed_methods=None, allowed_headers=None):
        """
        Assert that the response contains the expected CORS headers.

        Args:
            response (Response): The HTTP response
            allowed_origins (str or list, optional): The expected value for Access-Control-Allow-Origin. Defaults to '*'.
            allowed_methods (list, optional): The expected value for Access-Control-Allow-Methods.
            allowed_headers (list, optional): The expected value for Access-Control-Allow-Headers.

        Asserts:
            That the response contains the expected CORS headers
        """
        if allowed_origins == "*":
            self.assertEqual(
                response.get("Access-Control-Allow-Origin", None),
                "*",
                "Expected Access-Control-Allow-Origin header to be '*'",
            )
        elif isinstance(allowed_origins, list):
            self.assertIn(
                response.get("Access-Control-Allow-Origin", None),
                allowed_origins,
                f"Expected Access-Control-Allow-Origin header to be one of {allowed_origins}",
            )
        else:
            self.assertEqual(
                response.get("Access-Control-Allow-Origin", None),
                allowed_origins,
                f"Expected Access-Control-Allow-Origin header to be '{allowed_origins}'",
            )

        if allowed_methods:
            expected_methods = ", ".join(allowed_methods) if isinstance(allowed_methods, list) else allowed_methods
            self.assertEqual(
                response.get("Access-Control-Allow-Methods", None),
                expected_methods,
                f"Expected Access-Control-Allow-Methods header to be '{expected_methods}'",
            )

        if allowed_headers:
            expected_headers = ", ".join(allowed_headers) if isinstance(allowed_headers, list) else allowed_headers
            self.assertEqual(
                response.get("Access-Control-Allow-Headers", None),
                expected_headers,
                f"Expected Access-Control-Allow-Headers header to be '{expected_headers}'",
            )

    def assert_cache_control(self, response, max_age=None, private=None, no_cache=None, no_store=None):
        """
        Assert that the response contains the expected Cache-Control header.

        Args:
            response (Response): The HTTP response
            max_age (int, optional): The expected max-age value
            private (bool, optional): Whether the Cache-Control header should include 'private'
            no_cache (bool, optional): Whether the Cache-Control header should include 'no-cache'
            no_store (bool, optional): Whether the Cache-Control header should include 'no-store'

        Asserts:
            That the response contains the expected Cache-Control header
        """
        cache_control = response.get("Cache-Control", "")

        if max_age is not None:
            self.assertIn(
                f"max-age={max_age}", cache_control, f"Expected Cache-Control header to include 'max-age={max_age}'"
            )

        if private:
            self.assertIn("private", cache_control, "Expected Cache-Control header to include 'private'")

        if no_cache:
            self.assertIn("no-cache", cache_control, "Expected Cache-Control header to include 'no-cache'")

        if no_store:
            self.assertIn("no-store", cache_control, "Expected Cache-Control header to include 'no-store'")

    def assert_template_used(self, response, template_name):
        """
        Assert that the response used the specified template.

        Args:
            response (Response): The HTTP response
            template_name (str): The name of the template

        Asserts:
            That the response used the specified template
        """
        self.assertTemplateUsed(response, template_name, f"Expected response to use template '{template_name}'")

    def assert_redirects_to_url(self, response, expected_url, status_code=302):
        """
        Assert that the response redirects to the specified URL.

        Args:
            response (Response): The HTTP response
            expected_url (str): The expected URL to redirect to
            status_code (int, optional): The expected status code. Defaults to 302.

        Asserts:
            That the response redirects to the expected URL with the expected status code
        """
        self.assertEqual(
            response.status_code, status_code, f"Expected status code {status_code}, got {response.status_code}"
        )
        self.assertEqual(response.url, expected_url, f"Expected redirect to '{expected_url}', got '{response.url}'")

    def assert_redirects_to_named_url(self, response, url_name, args=None, kwargs=None, status_code=302):
        """
        Assert that the response redirects to the specified named URL.

        Args:
            response (Response): The HTTP response
            url_name (str): The name of the URL to redirect to
            args (list, optional): Positional arguments for the URL
            kwargs (dict, optional): Keyword arguments for the URL
            status_code (int, optional): The expected status code. Defaults to 302.

        Asserts:
            That the response redirects to the expected named URL with the expected status code
        """
        expected_url = reverse(url_name, args=args, kwargs=kwargs)
        self.assertEqual(
            response.status_code, status_code, f"Expected status code {status_code}, got {response.status_code}"
        )
        self.assertEqual(response.url, expected_url, f"Expected redirect to '{expected_url}', got '{response.url}'")

    def assert_form_valid(self, response, form_name="form"):
        """
        Assert that the form in the response is valid.

        Args:
            response (Response): The HTTP response
            form_name (str, optional): The name of the form in the context. Defaults to 'form'.

        Asserts:
            That the form in the response context is valid
        """
        self.assertIn(form_name, response.context, f"Expected response context to contain form '{form_name}'")
        form = response.context[form_name]
        self.assertTrue(form.is_valid(), f"Expected form '{form_name}' to be valid, but it has errors: {form.errors}")

    def assert_form_invalid(self, response, form_name="form"):
        """
        Assert that the form in the response is invalid.

        Args:
            response (Response): The HTTP response
            form_name (str, optional): The name of the form in the context. Defaults to 'form'.

        Asserts:
            That the form in the response context is invalid

        Returns:
            The form errors
        """
        self.assertIn(form_name, response.context, f"Expected response context to contain form '{form_name}'")
        form = response.context[form_name]
        self.assertFalse(form.is_valid(), f"Expected form '{form_name}' to be invalid, but it is valid")
        return form.errors

    def assert_message_exists(self, response, message_text=None, level=None):
        """
        Assert that the response contains a message.

        Args:
            response (Response): The HTTP response
            message_text (str, optional): The expected message text
            level (int, optional): The expected message level

        Asserts:
            That the response contains a message with the expected text and level

        Returns:
            The matching message, or None if no match was found
        """
        messages = list(response.context.get("messages", []))

        if not messages:
            self.fail("Expected response to contain messages, but none were found")

        for message in messages:
            if message_text and level:
                if message.message == message_text and message.level == level:
                    return message
            elif message_text:
                if message.message == message_text:
                    return message
            elif level:
                if message.level == level:
                    return message

        if message_text and level:
            self.fail(
                f"Expected response to contain message with text '{message_text}' and level {level}, but none was found"
            )
        elif message_text:
            self.fail(f"Expected response to contain message with text '{message_text}', but none was found")
        elif level:
            self.fail(f"Expected response to contain message with level {level}, but none was found")

        return None

    def assert_api_response(self, response, status_code=200, content_type="application/json", expected_data=None):
        """
        Assert that the response is a valid API response.

        Args:
            response (Response): The HTTP response
            status_code (int, optional): The expected status code. Defaults to 200.
            content_type (str, optional): The expected content type. Defaults to 'application/json'.
            expected_data (dict, optional): Expected data in the JSON response

        Asserts:
            That the response has the expected status code and content type
            If expected_data is provided, also asserts that the JSON contains the expected data

        Returns:
            The parsed JSON data
        """
        self._assert_http_status(status_code, response)
        self.assert_content_type(response, content_type)

        import json

        try:
            data = json.loads(response.content.decode("utf-8"))
        except json.JSONDecodeError:
            self.fail(f"Response does not contain valid JSON: {response.content}")

        if expected_data:
            for key, value in expected_data.items():
                self.assertIn(key, data, f"Expected JSON to contain key '{key}'")
                self.assertEqual(data[key], value, f"Expected key '{key}' to have value '{value}', got '{data[key]}'")

        return data

    def assert_api_error_response(self, response, status_code=400, error_key="error"):
        """
        Assert that the response is a valid API error response.

        Args:
            response (Response): The HTTP response
            status_code (int, optional): The expected status code. Defaults to 400.
            error_key (str, optional): The key in the JSON that contains the error message. Defaults to 'error'.

        Asserts:
            That the response has the expected status code and contains an error message

        Returns:
            The error message
        """
        self._assert_http_status(status_code, response)
        self.assert_content_type(response, "application/json")

        import json

        try:
            data = json.loads(response.content.decode("utf-8"))
        except json.JSONDecodeError:
            self.fail(f"Response does not contain valid JSON: {response.content}")

        self.assertIn(error_key, data, f"Expected JSON to contain error key '{error_key}'")
        self.assertIsNotNone(data[error_key], f"Expected error key '{error_key}' to have a value")

        return data[error_key]

    def assert_file_response(self, response, content_type=None, filename=None, file_content=None):
        """
        Assert that the response is a valid file download.

        Args:
            response (Response): The HTTP response
            content_type (str, optional): The expected content type
            filename (str, optional): The expected filename in the Content-Disposition header
            file_content (bytes, optional): The expected file content

        Asserts:
            That the response is a valid file download with the expected properties
        """
        self.assert_http_200_ok(response)

        if content_type:
            self.assert_content_type(response, content_type)

        if filename:
            self.assertIn("Content-Disposition", response, "Expected response to contain Content-Disposition header")
            self.assertIn(
                f'filename="{filename}"',
                response["Content-Disposition"],
                f"Expected Content-Disposition header to include filename='{filename}'",
            )

        if file_content:
            self.assertEqual(response.content, file_content, "Expected file content to match")

    def assert_view_class(self, view_func, expected_class):
        """
        Assert that the view function is an instance of the expected class.

        Args:
            view_func: The view function to check
            expected_class: The expected class

        Asserts:
            That the view function is an instance of the expected class
        """
        from django.views.generic import View

        if not issubclass(expected_class, View):
            self.fail(f"Expected class {expected_class.__name__} to be a subclass of View")

        view_class = view_func.view_class if hasattr(view_func, "view_class") else None
        self.assertEqual(
            view_class,
            expected_class,
            f"Expected view to be an instance of {expected_class.__name__}, got {view_class.__name__ if view_class else 'None'}",
        )

    def assert_view_permissions(self, url, permission, method="get", data=None):
        """
        Assert that the view requires the specified permission.

        Args:
            url (str): The URL to test
            permission (str): The permission to check (e.g., 'app_label.change_model')
            method (str, optional): The HTTP method to use. Defaults to 'get'.
            data (dict, optional): Data to send with the request

        Asserts:
            That the view requires the specified permission
        """
        # Create a user without the permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        no_perm_user = self.create_user(username="no_perm_user", password="test_password")
        self.client.login(username="no_perm_user", password="test_password")

        # Make the request
        request_method = getattr(self.client, method.lower())
        response = request_method(url, data=data)

        # Check that the response is a 403 Forbidden
        self.assert_http_403_forbidden(response)

        # Now add the permission and try again
        app_label, codename = permission.split(".")
        content_type = ContentType.objects.get(app_label=app_label)
        permission_obj = Permission.objects.get(content_type=content_type, codename=codename)
        no_perm_user.user_permissions.add(permission_obj)

        # Make the request again
        response = request_method(url, data=data)

        # Check that the response is not a 403 Forbidden
        self.assertNotEqual(
            response.status_code,
            403,
            f"Expected response status code to not be 403 after adding permission, got {response.status_code}",
        )

    def assert_query_count(self, func, expected_count, *args, **kwargs):
        """
        Assert that the function executes the expected number of database queries.

        Args:
            func: The function to execute
            expected_count (int): The expected number of queries
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Asserts:
            That the function executes the expected number of queries

        Returns:
            The result of the function
        """
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        with CaptureQueriesContext(connection) as context:
            result = func(*args, **kwargs)

        query_count = len(context.captured_queries)
        self.assertEqual(query_count, expected_count, f"Expected {expected_count} queries, got {query_count}")

        return result
