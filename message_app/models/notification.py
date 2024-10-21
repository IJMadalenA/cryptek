from django.db.models import Model, CASCADE, TextField, ForeignKey, BooleanField, DateTimeField

from conscious_element.models.cryptek_user import CryptekUser


class Notification(Model):
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name='notifications')
    message = TextField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def str(self):
        return f'Notification for {self.user}'
