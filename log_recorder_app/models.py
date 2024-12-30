from django.db.models import (CASCADE, DateTimeField, ForeignKey, Model,
                              TextField)

from conscious_element.models.cryptek_user import CryptekUser


# AuditLog model
class AuditLog(Model):
    user = ForeignKey(CryptekUser, on_delete=CASCADE, related_name="audit_logs")
    action = TextField()
    action_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit log for {self.user.username}"
