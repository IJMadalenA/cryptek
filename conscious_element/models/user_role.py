from django.db.models import CASCADE, CharField, ForeignKey, Model

from conscious_element.models.cryptek_user import CryptekUser


class UserRole(Model):
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="roles")
    role = CharField(max_length=50)  # e.g., 'admin', 'editor', 'author'

    def str(self):
        return f"{self.user.username} is a {self.role}"
