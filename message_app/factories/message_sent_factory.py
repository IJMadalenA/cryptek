from factory import SubFactory
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from message_app.models.message_sent import MessageSent


class MessageSentFactory(DjangoModelFactory):
    user_sender = SubFactory(CryptekUserFactory)

    class Meta:
        model = MessageSent
