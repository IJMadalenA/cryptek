from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyChoice

from conscious_element.models.blocked_email_domain import BlockedEmailDomain, BlockedEmailDomainExtension


class BlockedEmailDomainFactory(DjangoModelFactory):
    username = Sequence(lambda n: f"blocked_user_{n}")
    domain = Sequence(lambda n: f"blocked_domain_{n}")
    added_at = FuzzyDateTime(start_dt=timezone.now())
    is_blocked = FuzzyChoice(choices=[True, False])
    domain_extension = None  # Assuming this is set to None for simplicity

    class Meta:
        model = BlockedEmailDomain


class BlockedEmailDomainExtensionFactory(DjangoModelFactory):
    domain_extension = Sequence(lambda n: f"blocked_extension_{n}")
    added_at = FuzzyDateTime(start_dt=timezone.now())
    is_blocked = FuzzyChoice(choices=[True, False])

    class Meta:
        model = BlockedEmailDomainExtension
