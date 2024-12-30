from datetime import timedelta, datetime

from django.utils.timezone import make_aware
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime
from factory import Sequence, SubFactory, LazyAttributeSequence, lazy_attribute_sequence, SelfAttribute

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from conscious_element.models.session import Session

class SessionFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    expire_date = FuzzyDateTime(
        start_dt=make_aware(datetime.now()),
        end_dt=make_aware(datetime.now() + timedelta(days=30)),
    ).fuzz()
    session_key = Sequence(lambda n: n)
    user_id = SelfAttribute('user.pk')

    class Meta:
        model = Session
