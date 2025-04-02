from django.contrib.auth import get_user_model

from cryptek.qa_templates import ClassBaseViewTestCase
from user_app.models.profile import Profile

User = get_user_model()


class UserProfileTestCase(ClassBaseViewTestCase):
    def setUp(self):
        """Set up two users with public and private profiles."""
        self.user_public = self.create_user(username="public_user", password="password123")
        self.profile_public = Profile.objects.create(user=self.user_public, visibility=Profile.Visibility.PUBLIC)

        self.user_private = self.create_user(username="private_user", password="password123")
        self.profile_private = Profile.objects.create(user=self.user_private, visibility=Profile.Visibility.PRIVATE)

    # def test_public_profile_access(self):
    #     """An unauthenticated user can view a public profile."""
    #     response = self.client.get(reverse("user_app:public_profile", args=[self.user_public.username]))
    #     self.assertEqual(response.status_code, 200)

    # def test_private_profile_access(self):
    #     """An unauthenticated user CANNOT view a private profile."""
    #     response = self.client.get(reverse("user_app:public_profile", args=[self.user_private.username]))
    #     self.assertRedirects(response, reverse("user_app:personal_profile"))

    # def test_user_cannot_edit_other_profile(self):
    #     """A user CANNOT edit another user's profile."""
    #     self.client.login(username="public_user", password="password123")
    #     response = self.client.post(reverse("user_app:edit_profile"), {"bio": "Hacked bio"})
    #     self.profile_private.refresh_from_db()
    #     self.assertNotEqual(self.profile_private.bio, "Hacked bio")
