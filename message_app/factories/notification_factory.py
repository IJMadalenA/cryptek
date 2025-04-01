from factory import SubFactory
from factory.django import DjangoModelFactory

from message_app.models.notification import Notification
from user_app.factory.cryptek_user_factory import CryptekUserFactory


class NotificationFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)

    class Meta:
        model = Notification
