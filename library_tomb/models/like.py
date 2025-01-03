from django.db.models import CASCADE, DateTimeField, ForeignKey, Model

from conscious_element.models.cryptek_user import CryptekUser
from library_tomb.models.entry import Entry


class Like(Model):
    entry = ForeignKey(Entry, on_delete=CASCADE, related_name="likes")
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="likes")
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.entry}"
