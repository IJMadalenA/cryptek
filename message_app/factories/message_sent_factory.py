from factory import SubFactory
from factory.django import DjangoModelFactory

from message_app.models.message_sent import MessageSent
from user_app.factory.cryptek_user_factory import CryptekUserFactory


class MessageSentFactory(DjangoModelFactory):
    user_sender = SubFactory(CryptekUserFactory)

    class Meta:
        model = MessageSent
