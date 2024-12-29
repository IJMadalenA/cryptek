from factory import Sequence
from factory.django import DjangoModelFactory

from conscious_element.models.cryptek_user import CryptekUser


class CryptekUserFactory(DjangoModelFactory):
    username = Sequence(lambda n: f"cryptek_user_{n}")
    email = Sequence(lambda n: f"www.user_{n}@cryptek.com")
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = CryptekUser
