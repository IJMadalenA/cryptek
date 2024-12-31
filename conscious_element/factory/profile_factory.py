from factory import SelfAttribute, SubFactory
from factory.django import DjangoModelFactory

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from conscious_element.models.profile import Profile


class ProfileFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    user_id = SelfAttribute("user.id")

    class Meta:
        model = Profile
