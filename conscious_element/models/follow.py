from django.db.models import Model, ForeignKey, CASCADE, DateTimeField

from conscious_element.models.cryptek_user import CryptekUser


# Follow model
class Follow(Model):
    follower = ForeignKey(CryptekUser, on_delete=CASCADE, related_name='following')
    following = ForeignKey(CryptekUser, on_delete=CASCADE, related_name='followers')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def str(self):
        return f'{self.follower.username} follows {self.following.username}'
