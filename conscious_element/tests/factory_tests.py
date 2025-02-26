from conscious_element.backends import SessionStore
from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from conscious_element.factory.follow_factory import FollowFactory
from conscious_element.factory.profile_factory import ProfileFactory
from conscious_element.factory.session_factory import SessionFactory
from cryptek.test_and_check.base_factory_test import BaseFactoryTest


class CryptekUserFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = CryptekUserFactory


class FollowFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = FollowFactory


class ProfileFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = ProfileFactory


class SessionsFactoryTestCase(BaseFactoryTest):
    def test_get_session_store_class_returns_correct_class(self):
        result = self.Meta.factory._meta.model.get_session_store_class()
        expected = SessionStore
        self.assertEqual(result, expected, "The method did not return SessionStore class.")
        self.assertIsInstance(
            result(),
            SessionStore,
            "The method did not return an instance of SessionStore class.",
        )

    def test_get_session_store_class_returns_correct_store(self):
        store_class = self.Meta.factory._meta.model.get_session_store_class()
        self.assertEqual(
            store_class,
            SessionStore,
            "Expected get_session_store_class to return the SessionStore class.",
        )

    class Meta:
        factory = SessionFactory


class UserFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = CryptekUserFactory
