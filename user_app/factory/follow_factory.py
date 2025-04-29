from factory import SelfAttribute, SubFactory
from factory.django import DjangoModelFactory
from user_app.factory.cryptek_user_factory import CryptekUserFactory
from user_app.models.follow import Follow


class FollowFactory(DjangoModelFactory):
    follower = SubFactory(CryptekUserFactory)
    follower_id = SelfAttribute("follower.id")
    following = SubFactory(CryptekUserFactory)
    following_id = SelfAttribute("following.id")

    class Meta:
        model = Follow
