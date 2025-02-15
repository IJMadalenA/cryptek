from cryptek.test_and_check.base_model_test import BaseModelTestCase
from message_app.factories.message_sent_factory import MessageSentFactory
from message_app.factories.notification_factory import NotificationFactory
from message_app.factories.social_share_factory import SocialShareFactory


class MessageSentModelTest(BaseModelTestCase):
    class Meta:
        factory = MessageSentFactory


class NotificationModelTest(BaseModelTestCase):
    class Meta:
        factory = NotificationFactory


class SocialShareModelTest(BaseModelTestCase):
    class Meta:
        factory = SocialShareFactory
