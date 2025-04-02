from cryptek.test_and_check.base_factory_test import BaseFactoryTest
from user_app.backends import SessionStore
from user_app.factory.blocked_email_domain_factory import BlockedEmailDomainExtensionFactory, BlockedEmailDomainFactory
from user_app.factory.cryptek_user_factory import CryptekUserFactory
from user_app.factory.follow_factory import FollowFactory
from user_app.factory.profile_factory import ProfileFactory
from user_app.factory.session_factory import SessionFactory


class BlockedEmailDomainFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = BlockedEmailDomainFactory


class BlockedEmailDomainExtensionFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = BlockedEmailDomainExtensionFactory


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
