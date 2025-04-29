import secrets

from cryptek.status_code_assertion import StatusCodeAssertionMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models import Q
from django.shortcuts import resolve_url
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import NoReverseMatch, reverse
from factory.fuzzy import FuzzyText

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
    """

    endpoint_name = None
    is_authenticated = None
    kwargs = None
    args = None

    def setUp(self):
        _password = secrets.token_urlsafe(16)
        self.client = Client()
        self.user_instance = self.create_user()
        self.user_instance.set_password(_password)
        self.user_instance.save()

        if isinstance(self.login, AbstractUser):
            username = self.login.username
        else:
            username = self.user_instance.username

        if isinstance(self.is_authenticated, bool):
            if self.is_authenticated:
                self.client.login(
                    username=username,
                    password=_password,
                )
                if not self.user_instance.is_authenticated:
                    raise Exception("The user was not able to authenticate.")
            else:
                self.client.logout()
        else:
            raise Exception("is_authenticated must set and be a boolean.")

        self.assertTrue(
            self.client.login(username=self.user_instance.username, password=_password),
            msg=f"Login failed - {self.user_instance.username} - {_password}",
        )

    @staticmethod
    def create_user(username="test_user", password="test_password"):
        return get_user_model().objects.create_user(username=username, password=password)

    def authenticate(self):
        self.client.login(username=self.login.username, password="password")

    def unauthenticated(self):
        self.client.logout()

    def get(self, *args, **kwargs):
        return self.client.get(path=reverse(self.endpoint_name, args=self.args, kwargs=self.kwargs), *args, **kwargs)

    def post(self, data, *args, **kwargs):
        return self.client.post(
            path=reverse(self.endpoint_name, args=self.args, kwargs=self.kwargs), data=data, *args, **kwargs
        )

    def put(self, data, *args, **kwargs):
        return self.client.put(
            path=reverse(self.endpoint_name, args=self.args, kwargs=self.kwargs), data=data, *args, **kwargs
        )

    def delete(self, *args, **kwargs):
        return self.client.delete(
            path=reverse(self.endpoint_name, args=self.args, kwargs=self.kwargs), *args, **kwargs
        )

    def get_check_200(self, url, *args, **kwargs):
        response = super(ClassBaseViewTestCase, self).get(url, *args, **kwargs)
        self.response_200(response)
        return response

    def assert_login_required(self, url, *args, **kwargs):
        """Ensure login is required to GET this URL"""
        response = super(ClassBaseViewTestCase, self).get(url, *args, **kwargs)
        reversed_url = reverse(url, args=args, kwargs=kwargs)
        login_url = str(resolve_url(settings.LOGIN_URL))
        expected_url = "{0}?next={1}".format(login_url, reversed_url)
        self.assertRedirects(response, expected_url)
