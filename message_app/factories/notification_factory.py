from factory import SubFactory
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from message_app.models.notification import Notification


class NotificationFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)

    class Meta:
        model = Notification
