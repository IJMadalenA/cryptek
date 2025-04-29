from factory import SelfAttribute, SubFactory
from factory.django import DjangoModelFactory
from user_app.factory.cryptek_user_factory import CryptekUserFactory
from user_app.models.profile import Profile


class ProfileFactory(DjangoModelFactory):
    user = SubFactory(CryptekUserFactory)
    user_id = SelfAttribute("user.id")

    class Meta:
        model = Profile
