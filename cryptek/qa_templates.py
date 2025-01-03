from django.test import TestCase
from factory.django import DjangoModelFactory


class BaseFactoryTest(TestCase):
    """
    Base test case for testing factory implementations.

    Provides functionality to test if a Django model factory is properly set up,
    correctly creates single instances, and supports batch creation of multiple
    instances. Designed to work with `factory_boy`'s `DjangoModelFactory`.
    This test case also allows marking test cases as abstract or skipping the
    tests if no factory is provided.

    Attributes:
        model: Class of the model associated with the factory defined in Meta.
    """

    def setUp(self):
        """
        setUp(self)

        Prepares the test case for execution by performing checks and initialization based
        on the Meta attribute provided in the test class. It ensures that a compatible
        factory and model are defined before executing the tests.

        Raises
        ------
        TypeError
            If the 'factory' defined in the Meta attribute is not a subclass of
            DjangoModelFactory.

        Skips
        -----
        If the Meta attribute does not define a 'factory' property or if the 'abstract'
        attribute of Meta is set to True, the test will be skipped to prevent execution.

        Notes
        -----
        This method verifies that:
        - 'Meta' and its 'factory' attribute are defined in the test class.
        - The 'abstract' field in the Meta attribute determines whether the tests
          should be executed.
        - The factory must be a subclass of DjangoModelFactory for compatibility.

        After validation, the corresponding model for the factory is set to
        self.model for further use.
        """
        if not hasattr(self, "Meta") or not hasattr(self.Meta, "factory"):
            self.skipTest("Skipping tests as no factory is defined in Meta.")
        if getattr(self.Meta, "abstract", False):
            self.skipTest("Skipping tests as this TestCase is marked abstract.")

        if not self.Meta.factory or not issubclass(
            self.Meta.factory, DjangoModelFactory
        ):
            raise TypeError(
                "The factory defined in Meta is not a subclass of DjangoModelFactory"
            )

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

    class Meta:
        abstract = True
        factory = None


from functools import partial

import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models import Q
from django.shortcuts import resolve_url
from django.test import RequestFactory
from django.test import TestCase as DjangoTestCase
from django.test import signals
from django.test.client import store_rendered_templates
from django.test.utils import CaptureQueriesContext

try:
    from django.urls import NoReverseMatch, reverse
except ImportError:
    from django.core.urlresolvers import NoReverseMatch, reverse  # noqa

try:
    import rest_framework  # noqa

    DRF = True
except ImportError:
    DRF = False


def get_api_client():
    try:
        from rest_framework.test import APIClient
    except ImportError:
        from django.core.exceptions import ImproperlyConfigured

        def APIClient(*args, **kwargs):
            raise ImproperlyConfigured(
                "django-rest-framework must be installed in order to use APITestCase."
            )

    return APIClient


if hasattr(DjangoTestCase, "assertURLEqual"):
    assertURLEqual = DjangoTestCase.assertURLEqual
else:

    def assertURLEqual(t, url1, url2, msg_prefix=""):
        raise NotImplementedError(
            "Your version of Django does not support `assertURLEqual`"
        )


class StatusCodeAssertionMixin(object):
    """
    The following `assert_http_###_status_name` methods were intentionally added statically instead of dynamically so
    that code completion in IDEs like PyCharm would work. It is preferred to use these methods over the response_XXX
    methods, which could be deprecated at some point. The assert methods contain both the number and the status name
    slug so that people that remember them best by their numeric code and people that remember best by their name will
    be able to easily find the assertion they need. This was also directly patterned off of what the `Django Rest
    Framework uses <https://github.com/encode/django-rest-framework/blob/main/rest_framework/status.py>`_.
    """

    def _assert_http_status(self, status_code, response=None, msg=None, url=None):
        response = self._which_response(response)
        self.assertEqual(response.status_code, status_code, msg)
        if url is not None:
            self.assertEqual(response.url, url)

    def assert_http_100_continue(self, response=None, msg=None):
        self._assert_http_status(100, response=response, msg=msg)

    def assert_http_101_switching_protocols(self, response=None, msg=None):
        self._assert_http_status(101, response=response, msg=msg)

    def assert_http_200_ok(self, response=None, msg=None):
        self._assert_http_status(200, response=response, msg=msg)

    def assert_http_201_created(self, response=None, msg=None):
        self._assert_http_status(201, response=response, msg=msg)

    def assert_http_202_accepted(self, response=None, msg=None):
        self._assert_http_status(202, response=response, msg=msg)

    def assert_http_203_non_authoritative_information(self, response=None, msg=None):
        self._assert_http_status(203, response=response, msg=msg)

    def assert_http_204_no_content(self, response=None, msg=None):
        self._assert_http_status(204, response=response, msg=msg)

    def assert_http_205_reset_content(self, response=None, msg=None):
        self._assert_http_status(205, response=response, msg=msg)

    def assert_http_206_partial_content(self, response=None, msg=None):
        self._assert_http_status(206, response=response, msg=msg)

    def assert_http_207_multi_status(self, response=None, msg=None):
        self._assert_http_status(207, response=response, msg=msg)

    def assert_http_208_already_reported(self, response=None, msg=None):
        self._assert_http_status(208, response=response, msg=msg)

    def assert_http_226_im_used(self, response=None, msg=None):
        self._assert_http_status(226, response=response, msg=msg)

    def assert_http_300_multiple_choices(self, response=None, msg=None):
        self._assert_http_status(300, response=response, msg=msg)

    def assert_http_301_moved_permanently(self, response=None, msg=None, url=None):
        self._assert_http_status(301, response=response, msg=msg, url=url)

    def assert_http_302_found(self, response=None, msg=None, url=None):
        self._assert_http_status(302, response=response, msg=msg, url=url)

    def assert_http_303_see_other(self, response=None, msg=None):
        self._assert_http_status(303, response=response, msg=msg)

    def assert_http_304_not_modified(self, response=None, msg=None):
        self._assert_http_status(304, response=response, msg=msg)

    def assert_http_305_use_proxy(self, response=None, msg=None):
        self._assert_http_status(305, response=response, msg=msg)

    def assert_http_306_reserved(self, response=None, msg=None):
        self._assert_http_status(306, response=response, msg=msg)

    def assert_http_307_temporary_redirect(self, response=None, msg=None):
        self._assert_http_status(307, response=response, msg=msg)

    def assert_http_308_permanent_redirect(self, response=None, msg=None):
        self._assert_http_status(308, response=response, msg=msg)

    def assert_http_400_bad_request(self, response=None, msg=None):
        self._assert_http_status(400, response=response, msg=msg)

    def assert_http_401_unauthorized(self, response=None, msg=None):
        self._assert_http_status(401, response=response, msg=msg)

    def assert_http_402_payment_required(self, response=None, msg=None):
        self._assert_http_status(402, response=response, msg=msg)

    def assert_http_403_forbidden(self, response=None, msg=None):
        self._assert_http_status(403, response=response, msg=msg)

    def assert_http_404_not_found(self, response=None, msg=None):
        self._assert_http_status(404, response=response, msg=msg)

    def assert_http_405_method_not_allowed(self, response=None, msg=None):
        self._assert_http_status(405, response=response, msg=msg)

    def assert_http_406_not_acceptable(self, response=None, msg=None):
        self._assert_http_status(406, response=response, msg=msg)

    def assert_http_407_proxy_authentication_required(self, response=None, msg=None):
        self._assert_http_status(407, response=response, msg=msg)

    def assert_http_408_request_timeout(self, response=None, msg=None):
        self._assert_http_status(408, response=response, msg=msg)

    def assert_http_409_conflict(self, response=None, msg=None):
        self._assert_http_status(409, response=response, msg=msg)

    def assert_http_410_gone(self, response=None, msg=None):
        self._assert_http_status(410, response=response, msg=msg)

    def assert_http_411_length_required(self, response=None, msg=None):
        self._assert_http_status(411, response=response, msg=msg)

    def assert_http_412_precondition_failed(self, response=None, msg=None):
        self._assert_http_status(412, response=response, msg=msg)

    def assert_http_413_request_entity_too_large(self, response=None, msg=None):
        self._assert_http_status(413, response=response, msg=msg)

    def assert_http_414_request_uri_too_long(self, response=None, msg=None):
        self._assert_http_status(414, response=response, msg=msg)

    def assert_http_415_unsupported_media_type(self, response=None, msg=None):
        self._assert_http_status(415, response=response, msg=msg)

    def assert_http_416_requested_range_not_satisfiable(self, response=None, msg=None):
        self._assert_http_status(416, response=response, msg=msg)

    def assert_http_417_expectation_failed(self, response=None, msg=None):
        self._assert_http_status(417, response=response, msg=msg)

    def assert_http_422_unprocessable_entity(self, response=None, msg=None):
        self._assert_http_status(422, response=response, msg=msg)

    def assert_http_423_locked(self, response=None, msg=None):
        self._assert_http_status(423, response=response, msg=msg)

    def assert_http_424_failed_dependency(self, response=None, msg=None):
        self._assert_http_status(424, response=response, msg=msg)

    def assert_http_426_upgrade_required(self, response=None, msg=None):
        self._assert_http_status(426, response=response, msg=msg)

    def assert_http_428_precondition_required(self, response=None, msg=None):
        self._assert_http_status(428, response=response, msg=msg)

    def assert_http_429_too_many_requests(self, response=None, msg=None):
        self._assert_http_status(429, response=response, msg=msg)

    def assert_http_431_request_header_fields_too_large(self, response=None, msg=None):
        self._assert_http_status(431, response=response, msg=msg)

    def assert_http_451_unavailable_for_legal_reasons(self, response=None, msg=None):
        self._assert_http_status(451, response=response, msg=msg)

    def assert_http_500_internal_server_error(self, response=None, msg=None):
        self._assert_http_status(500, response=response, msg=msg)

    def assert_http_501_not_implemented(self, response=None, msg=None):
        self._assert_http_status(501, response=response, msg=msg)

    def assert_http_502_bad_gateway(self, response=None, msg=None):
        self._assert_http_status(502, response=response, msg=msg)

    def assert_http_503_service_unavailable(self, response=None, msg=None):
        self._assert_http_status(503, response=response, msg=msg)

    def assert_http_504_gateway_timeout(self, response=None, msg=None):
        self._assert_http_status(504, response=response, msg=msg)

    def assert_http_505_http_version_not_supported(self, response=None, msg=None):
        self._assert_http_status(505, response=response, msg=msg)

    def assert_http_506_variant_also_negotiates(self, response=None, msg=None):
        self._assert_http_status(506, response=response, msg=msg)

    def assert_http_507_insufficient_storage(self, response=None, msg=None):
        self._assert_http_status(507, response=response, msg=msg)

    def assert_http_508_loop_detected(self, response=None, msg=None):
        self._assert_http_status(508, response=response, msg=msg)

    def assert_http_509_bandwidth_limit_exceeded(self, response=None, msg=None):
        self._assert_http_status(509, response=response, msg=msg)

    def assert_http_510_not_extended(self, response=None, msg=None):
        self._assert_http_status(510, response=response, msg=msg)

    def assert_http_511_network_authentication_required(self, response=None, msg=None):
        self._assert_http_status(511, response=response, msg=msg)


class NoPreviousResponse(Exception):
    pass


# Build a real context

CAPTURE = True


class _AssertNumQueriesLessThanContext(CaptureQueriesContext):
    def __init__(self, test_case, num, connection, verbose=False):
        self.test_case = test_case
        self.num = num
        self.verbose = verbose
        super(_AssertNumQueriesLessThanContext, self).__init__(connection)

    def __exit__(self, exc_type, exc_value, traceback):
        super(_AssertNumQueriesLessThanContext, self).__exit__(
            exc_type, exc_value, traceback
        )
        if exc_type is not None:
            return
        executed = len(self)
        msg = "%d queries executed, expected less than %d" % (executed, self.num)
        if self.verbose:
            queries = "\n\n".join(q["sql"] for q in self.captured_queries)
            msg += ". Executed queries were:\n\n%s" % queries
        self.test_case.assertLess(executed, self.num, msg)


class login(object):
    """
    A useful login context for Django tests.  If the first argument is
    a User, we will login with that user's username.  If no password is
    given we will use 'password'.
    """

    def __init__(self, testcase, *args, **credentials):
        self.testcase = testcase
        user = get_user_model()

        if args and isinstance(args[0], user):
            username_field = getattr(user, "USERNAME_FIELD", "username")
            credentials.update(
                {
                    username_field: getattr(args[0], username_field),
                }
            )

        if not credentials.get("password", False):
            credentials["password"] = "password"

        success = testcase.client.login(**credentials)
        self.testcase.assertTrue(
            success, "login failed with credentials=%r" % credentials
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class BaseTestCase(StatusCodeAssertionMixin):
    """
    Django TestCase with helpful additional features
    """

    user_factory = None

    def __init__(self, *args, **kwargs):
        self.last_response = None

    def tear_down(self):
        self.client.logout()

    def print_form_errors(self, response_or_form=None):
        """A utility method for quickly debugging responses with form errors."""

        if response_or_form is None:
            response_or_form = self.last_response

        if hasattr(response_or_form, "errors"):
            form = response_or_form
        elif hasattr(response_or_form, "context"):
            form = response_or_form.context["form"]
        else:
            raise Exception(
                "print_form_errors requires the response_or_form argument to either be a Django http response or a form instance."
            )

        print(form.errors.as_text())

    def request(self, method_name, url_name, *args, **kwargs):
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
                **extra
            )
        except NoReverseMatch:
            self.last_response = method(url_name, data=data, follow=follow, **extra)

        self.context = self.last_response.context
        return self.last_response

    def get(self, url_name, *args, **kwargs):
        return self.request("get", url_name, *args, **kwargs)

    def post(self, url_name, *args, **kwargs):
        return self.request("post", url_name, *args, **kwargs)

    def put(self, url_name, *args, **kwargs):
        return self.request("put", url_name, *args, **kwargs)

    def patch(self, url_name, *args, **kwargs):
        return self.request("patch", url_name, *args, **kwargs)

    def head(self, url_name, *args, **kwargs):
        return self.request("head", url_name, *args, **kwargs)

    def options(self, url_name, *args, **kwargs):
        return self.request("options", url_name, *args, **kwargs)

    def delete(self, url_name, *args, **kwargs):
        return self.request("delete", url_name, *args, **kwargs)

    def _which_response(self, response=None):
        if response is None and self.last_response is not None:
            return self.last_response
        else:
            return response

    def _assert_response_code(self, status_code, response=None, msg=None):
        response = self._which_response(response)
        self.assertEqual(response.status_code, status_code, msg)

    def response_200(self, response=None, msg=None):
        """Given response has status_code 200"""
        self._assert_response_code(200, response, msg)

    def response_201(self, response=None, msg=None):
        """Given response has status_code 201"""
        self._assert_response_code(201, response, msg)

    def response_204(self, response=None, msg=None):
        """Given response has status_code 204"""
        self._assert_response_code(204, response, msg)

    def response_301(self, response=None, msg=None):
        """Given response has status_code 301"""
        self._assert_response_code(301, response, msg)

    def response_302(self, response=None, msg=None):
        """Given response has status_code 302"""
        self._assert_response_code(302, response, msg)

    def response_400(self, response=None, msg=None):
        """Given response has status_code 400"""
        self._assert_response_code(400, response, msg)

    def response_401(self, response=None, msg=None):
        """Given response has status_code 401"""
        self._assert_response_code(401, response, msg)

    def response_403(self, response=None, msg=None):
        """Given response has status_code 403"""
        self._assert_response_code(403, response, msg)

    def response_404(self, response=None, msg=None):
        """Given response has status_code 404"""
        self._assert_response_code(404, response, msg)

    def response_405(self, response=None, msg=None):
        """Given response has status_code 405"""
        self._assert_response_code(405, response, msg)

    def response_409(self, response=None, msg=None):
        """Given response has status_code 409"""
        self._assert_response_code(409, response, msg)

    def response_410(self, response=None, msg=None):
        """Given response has status_code 410"""
        self._assert_response_code(410, response, msg)

    def get_check_200(self, url, *args, **kwargs):
        """Test that we can GET a page and it returns a 200"""
        response = self.get(url, *args, **kwargs)
        self.response_200(response)
        return response

    def assertLoginRequired(self, url, *args, **kwargs):
        """Ensure login is required to GET this URL"""
        response = self.get(url, *args, **kwargs)
        reversed_url = reverse(url, args=args, kwargs=kwargs)
        login_url = str(resolve_url(settings.LOGIN_URL))
        expected_url = "{0}?next={1}".format(login_url, reversed_url)
        self.assertRedirects(response, expected_url)

    assertRedirects = DjangoTestCase.assertRedirects
    assertURLEqual = assertURLEqual

    def login(self, *args, **credentials):
        """Login a user"""
        return login(self, *args, **credentials)

    def reverse(self, name, *args, **kwargs):
        """Reverse a url, convenience to avoid having to import reverse in tests"""
        return reverse(name, args=args, kwargs=kwargs)

    @classmethod
    def make_user(cls, username="testuser", password="password", perms=None):
        """
        Build a user with <username> and password of 'password' for testing
        purposes.
        """
        if cls.user_factory:
            User = cls.user_factory._meta.model
            user_factory = cls.user_factory
        else:
            User = get_user_model()
            user_factory = User.objects.create_user

        USERNAME_FIELD = getattr(User, "USERNAME_FIELD", "username")
        user_data = {USERNAME_FIELD: username}
        EMAIL_FIELD = getattr(User, "EMAIL_FIELD", None)
        if EMAIL_FIELD is not None and cls.user_factory is None:
            user_data[EMAIL_FIELD] = "{}@example.com".format(username)
        test_user = user_factory(**user_data)
        test_user.set_password(password)
        test_user.save()

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
                    _filter = _filter | Q(
                        content_type__app_label=app_label, codename=codename
                    )

            test_user.user_permissions.add(*list(Permission.objects.filter(_filter)))

        return test_user

    def assertNumQueriesLessThan(self, num, *args, **kwargs):
        func = kwargs.pop("func", None)
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        verbose = kwargs.pop("verbose", False)
        conn = connections[using]

        context = _AssertNumQueriesLessThanContext(self, num, conn, verbose=verbose)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)

    def assertGoodView(self, url_name, *args, verbose=False, **kwargs):
        """
        Quick-n-dirty testing of a given url name.
        Ensures URL returns a 200 status and that generates less than 50
        database queries.
        """
        query_count = kwargs.pop("test_query_count", 50)

        with self.assertNumQueriesLessThan(query_count, verbose=verbose):
            response = self.get(url_name, *args, **kwargs)

        self.response_200(response)

        return response

    def assertResponseContains(self, text, response=None, html=True, **kwargs):
        """Convenience wrapper for assertContains"""
        response = self._which_response(response)
        self.assertContains(response, text, html=html, **kwargs)

    def assertResponseNotContains(self, text, response=None, html=True, **kwargs):
        """Convenience wrapper for assertNotContains"""
        response = self._which_response(response)
        self.assertNotContains(response, text, html=html, **kwargs)

    def assertResponseHeaders(self, headers, response=None):
        """
        Check that the headers in the response are as expected.

        Only headers defined in `headers` are compared, other keys present on
        the `response` will be ignored.

        :param headers: Mapping of header names to expected values
        :type headers: :class:`collections.Mapping`
        :param response: Response to check headers against
        :type response: :class:`django.http.response.HttpResponse`
        """
        response = self._which_response(response)
        compare = {h: response.get(h) for h in headers}
        self.assertEqual(compare, headers)

    def get_context(self, key):
        if self.last_response is not None:
            self.assertIn(key, self.last_response.context)
            return self.last_response.context[key]
        else:
            raise NoPreviousResponse("There isn't a previous response to query")

    def assertInContext(self, key):
        return self.get_context(key)

    def assertContext(self, key, value):
        self.assertEqual(self.get_context(key), value)


class TestCase(DjangoTestCase, BaseTestCase):
    """
    Django TestCase with helpful additional features
    """

    user_factory = None

    def __init__(self, *args, **kwargs):
        self.last_response = None
        super(TestCase, self).__init__(*args, **kwargs)


class APITestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self.client_class = get_api_client()
        super(APITestCase, self).__init__(*args, **kwargs)


# Note this class inherits from TestCase defined above.
class CBVTestCase(TestCase):
    """
    Directly calls class-based generic view methods,
    bypassing the Django test Client.

    This process bypasses middleware invocation and URL resolvers.

    Example usage:

        from myapp.views import MyClass

        class MyClassTest(CBVTestCase):

            def test_special_method(self):
                request = RequestFactory().get('/')
                instance = self.get_instance(MyClass, request=request)

                # invoke a MyClass method
                result = instance.special_method()

                # make assertions
                self.assertTrue(result)
    """

    @staticmethod
    def get_instance(view_cls, *args, **kwargs):
        """
        Returns a decorated instance of a class-based generic view class.

        Use `initkwargs` to set expected class attributes.
        For example, set the `object` attribute on MyDetailView class:

            instance = self.get_instance(MyDetailView, initkwargs={'object': obj}, request)

        because SingleObjectMixin (part of generic.DetailView)
        expects self.object to be set before invoking get_context_data().

        Pass a "request" kwarg in order for your tests to have particular
        request attributes.
        """
        initkwargs = kwargs.pop("initkwargs", None)
        request = kwargs.pop("request", None)
        if initkwargs is None:
            initkwargs = {}
        instance = view_cls(**initkwargs)
        instance.request = request
        instance.args = args
        instance.kwargs = kwargs
        return instance

    def get(self, view_cls, *args, **kwargs):
        """
        Calls view_cls.get() method after instantiating view class.
        Renders view templates and sets context if appropriate.
        """
        data = kwargs.pop("data", None)
        instance = self.get_instance(view_cls, *args, **kwargs)
        if not instance.request:
            # Use a basic request
            instance.request = RequestFactory().get("/", data)
        self.last_response = self.get_response(instance.request, instance.get)
        self.context = self.last_response.context
        return self.last_response

    def post(self, view_cls, *args, **kwargs):
        """
        Calls view_cls.post() method after instantiating view class.
        Renders view templates and sets context if appropriate.
        """
        data = kwargs.pop("data", None)
        if data is None:
            data = {}
        instance = self.get_instance(view_cls, *args, **kwargs)
        if not instance.request:
            # Use a basic request
            instance.request = RequestFactory().post("/", data)
        self.last_response = self.get_response(instance.request, instance.entry)
        self.context = self.last_response.context
        return self.last_response

    def get_response(self, request, view_func):
        """
        Obtain response from view class method (typically get or post).

        No middleware is invoked, but templates are rendered
        and context saved if appropriate.
        """
        # Curry (using functools.partial) a data dictionary into
        # an instance of the template renderer callback function.
        data = {}
        on_template_render = partial(store_rendered_templates, data)
        signal_uid = "template-render-%s" % id(request)
        signals.template_rendered.connect(on_template_render, dispatch_uid=signal_uid)
        try:
            response = view_func(request)

            if hasattr(response, "render") and callable(response.render):
                response = response.render()
                # Add any rendered template detail to the response.
                response.templates = data.get("templates", [])
                response.context = data.get("context")
            else:
                response.templates = None
                response.context = None

            return response
        finally:
            signals.template_rendered.disconnect(dispatch_uid=signal_uid)

    def get_check_200(self, url, *args, **kwargs):
        """Test that we can GET a page and it returns a 200"""
        response = super(CBVTestCase, self).get(url, *args, **kwargs)
        self.response_200(response)
        return response

    def assertLoginRequired(self, url, *args, **kwargs):
        """Ensure login is required to GET this URL"""
        response = super(CBVTestCase, self).get(url, *args, **kwargs)
        reversed_url = reverse(url, args=args, kwargs=kwargs)
        login_url = str(resolve_url(settings.LOGIN_URL))
        expected_url = "{0}?next={1}".format(login_url, reversed_url)
        self.assertRedirects(response, expected_url)

    def assertGoodView(self, url_name, *args, **kwargs):
        """
        Quick-n-dirty testing of a given view.
        Ensures view returns a 200 status and that generates less than 50
        database queries.
        """
        query_count = kwargs.pop("test_query_count", 50)

        with self.assertNumQueriesLessThan(query_count):
            response = super(CBVTestCase, self).get(url_name, *args, **kwargs)
        self.response_200(response)
        return response
