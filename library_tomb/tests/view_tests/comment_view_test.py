import json
import time
import unittest
from random import randint

from conscious_element.factory.cryptek_user_factory import CryptekUserFactory
from cryptek.qa_templates import ClassBaseViewTestCase
from library_tomb.factories.comment_factory import CommentFactory
from library_tomb.factories.entry_factory import EntryFactory
from library_tomb.models.comment import Comment


class CommentViewGetPostTestCase(ClassBaseViewTestCase):
    endpoint_name = "get_post_comment"
    is_authenticated = True

    def setUp(self):
        self.entry = EntryFactory.create(status=1)
        CommentFactory.create_batch(randint(3, 6), entry=self.entry)
        CommentFactory.create_batch(randint(3, 6))
        self.kwargs = {"slug": self.entry.slug}
        super().setUp()

    def test_get_comments(self):
        response = self.get()
        self.response_code(response=response, status_code=200)
        response_data = json.loads(response.content)
        self.assertIn("comments", response_data)
        self.assertTrue(len(response_data["comments"]) > 0)

    def test_all_comments_are_of_the_same_entry(self):
        response = self.get()
        response_data = json.loads(response.content)
        for comment in response_data["comments"]:
            self.assertEqual(comment.get("entry_id", None), self.entry.id)

    def test_get_login(self):
        with self.login():
            response = self.get()
            self.response_code(response=response, status_code=200)
            # Validate that the user is authenticated.
            response_data = json.loads(response.content)
            self.assertIn("comments", response_data)
            self.assertTrue(len(response_data["comments"]) > 0)

    def test_get_logout(self):
        with self.logout():
            response = self.get()
            self.response_code(response=response, status_code=200)
            # Validate that the user is authenticated.
            response_data = json.loads(response.content)
            self.assertIn("comments", response_data)
            self.assertTrue(len(response_data["comments"]) > 0)

    def test_get_login_with_instance(self):
        user_instance = CryptekUserFactory.create()
        with self.login(user_instance):
            response = self.get()
            self.response_code(response=response, status_code=200)
            # Validate that the user is authenticated.
            response_data = json.loads(response.content)
            self.assertIn("comments", response_data)
            self.assertTrue(len(response_data["comments"]) > 0)

    def test_post_comment(self):
        data = {"content": "This is a good comment."}
        response = self.post(data=data)
        self.response_code(response=response, status_code=201)
        response_data = json.loads(response.content)
        self.assertIn("message", response_data)

    def test_post_verified_comment(self):
        random_comment = randint(100000, 999999)
        data = {"content": f"This is a good comment - {random_comment}."}
        response = self.post(data=data)
        self.response_code(response=response, status_code=201)
        Comment.objects.filter(content=f"This is a good comment - {random_comment}.").exists()

    def test_post_moderation_system(self):
        data = {"content": f"This is a shitty comment"}
        response = self.post(data=data)
        self.response_code(response=response, status_code=400)
        Comment.objects.filter(content=f"This is a shitty comment").exists()

    def test_post_comment_invalid_data(self):
        data = {"content": ""}
        response = self.post(data=data)
        self.response_400(response)
        response_data = json.loads(response.content)
        self.assertIn("errors", response_data)

    def test_post_comment_unauthenticated(self):
        with self.logout():
            data = {"content": "This is a test comment."}
            response = self.post(data=data)
            self.response_code(response=response, status_code=302)

    @unittest.skipIf(condition=True, reason="Skipping this test because it takes too long running.")
    def test_rate_limiting(self):
        wait_time = 60
        time.sleep(wait_time)

        # Successfully post a comment.
        for _ in range(10):
            data = {"content": "This is a test comment."}
            response = self.post(data=data)
            self.response_code(response=response, status_code=201)

        # Comments not allowed.
        data = {"content": "This is a test comment."}
        response = self.post(data=data)
        self.response_code(response=response, status_code=403)

        # Wait for the rate limit to expire.
        time.sleep(wait_time)

        # Successfully post a comment after the rate limit has expired.
        for _ in range(5):
            data = {"content": "This is a test comment."}
            response = self.post(data=data)
            self.response_code(response=response, status_code=201)


class CommentViewPutDeleteTestCase(ClassBaseViewTestCase):
    endpoint_name = "put_delete_comment"
    is_authenticated = True

    def setUp(self):
        super().setUp()
        self.comment = CommentFactory.create(user=self.user_instance)
        self.kwargs = {"slug": self.comment.entry.slug, "pk": self.comment.id}
        self.user_instance.is_staff = True
        self.user_instance.save()

    def test_put_comment(self):
        data = {"content": "This is a very good comment."}
        response = self.put(data=data)
        self.response_code(response=response, status_code=200)
        response_data = json.loads(response.content)
        self.assertIn("message", response_data)

    def test_put_comment_invalid_data(self):
        data = {"content": ""}
        response = self.put(data=data)
        self.response_400(response)
        response_data = json.loads(response.content)
        self.assertFalse(response_data.get("success", None))

    def test_put_comment_unauthenticated(self):
        with self.logout():
            data = {"content": "This is an updated comment."}
            response = self.put(data=data)
            self.response_code(response=response, status_code=302)

    def test_delete_comment(self):
        response = self.delete()
        self.response_code(response=response, status_code=200)
        response_data = json.loads(response.content)
        self.assertIn("message", response_data)

    def test_delete_comment_unauthenticated(self):
        with self.logout():
            response = self.delete()
            self.response_code(response=response, status_code=302)

    def test_delete_comment_staff(self):
        self.comment.user.is_staff = True
        self.comment.user.save()
        response = self.delete()
        self.response_code(response=response, status_code=200)
        response_data = json.loads(response.content)
        self.assertIn("message", response_data)
