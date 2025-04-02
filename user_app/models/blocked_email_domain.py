from django.db.models import CASCADE, BooleanField, CharField, DateTimeField, ForeignKey, Model


class BlockedEmailDomainExtension(Model):
    domain_extension = CharField(max_length=255, unique=True)
    added_at = DateTimeField(auto_now_add=True)
    is_blocked = BooleanField(default=True)

    def __str__(self):
        return self.domain_extension


class BlockedEmailDomain(Model):
    username = CharField(max_length=255, unique=True)
    domain = CharField(max_length=255, unique=True)
    added_at = DateTimeField(auto_now_add=True)
    is_blocked = BooleanField(default=True)
    domain_extension = ForeignKey(
        BlockedEmailDomainExtension,
        on_delete=CASCADE,
        related_name="blocked_email_domains",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.domain
