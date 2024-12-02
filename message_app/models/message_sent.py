from django.db.models import (DO_NOTHING, BooleanField, CharField,
                              DateTimeField, EmailField, ForeignKey, Model,
                              TextField)

from conscious_element.models.cryptek_user import CryptekUser


class MessageSent(Model):
    class Meta:
        verbose_name = "Message Sent"
        verbose_name_plural = "Messages Sent"

    user_sender = ForeignKey(CryptekUser, on_delete=DO_NOTHING)
    email_sender = EmailField()
    first_name_sender = CharField()
    last_name_sender = CharField()
    message = TextField()
    date_sent = DateTimeField(auto_now_add=True)
    user_authenticated = BooleanField(
        default=False,
    )
