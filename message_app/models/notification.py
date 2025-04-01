from django.db.models import (CASCADE, BooleanField, DateTimeField, ForeignKey,
                              Model, TextField)

from user_app.models.cryptek_user import CryptekUser


class Notification(Model):
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="notifications")
    message = TextField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"
