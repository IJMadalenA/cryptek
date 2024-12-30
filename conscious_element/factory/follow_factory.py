from factory.django import DjangoModelFactory
from factory import SubFactory, SelfAttribute
from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from conscious_element.models.follow import Follow


class FollowFactory(DjangoModelFactory):
    follower = SubFactory(CryptekUserFactory)
    follower_id = SelfAttribute("follower.id")
    following = SubFactory(CryptekUserFactory)
    following_id = SelfAttribute("following.id")
    class Meta:
        model = Follow
