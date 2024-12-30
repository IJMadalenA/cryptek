from cryptek.qa_templates import BaseFactoryTest
from message_app.factories.message_sent_factory import MessageSentFactory
from message_app.factories.notification_factory import NotificationFactory
from message_app.factories.social_share_factory import SocialShareFactory


class MessageSentFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = MessageSentFactory


class NotificationFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = NotificationFactory


class SocialShareFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = SocialShareFactory
