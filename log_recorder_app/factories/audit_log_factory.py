from django.utils import timezone
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyText
from user_app.factory.cryptek_user_factory import CryptekUserFactory


class AuditLogFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    action = FuzzyText(length=120)
    action_date = FuzzyDateTime(start_dt=timezone.now())

    class Meta:
        model = "log_recorder_app.AuditLog"
