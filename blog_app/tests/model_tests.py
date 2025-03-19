from blog_app.factories.category_factory import CategoryFactory
from blog_app.factories.comment_factory import CommentFactory
from blog_app.factories.entry_factory import EntryFactory
from blog_app.factories.like_factory import LikeFactory
from blog_app.factories.multimedia_factory import MultimediaFactory
from blog_app.factories.tag_factory import TagFactory
from cryptek.test_and_check.base_model_test import BaseModelTestCase


class CategoryTestCase(BaseModelTestCase):
    class Meta:
        factory = CategoryFactory


class CommentTestCase(BaseModelTestCase):
    class Meta:
        factory = CommentFactory


class EntryTestCase(BaseModelTestCase):
    class Meta:
        factory = EntryFactory


class LikeTestCase(BaseModelTestCase):
    class Meta:
        factory = LikeFactory


class MultimediaTestCase(BaseModelTestCase):
    class Meta:
        factory = MultimediaFactory


class TagTestCase(BaseModelTestCase):
    class Meta:
        factory = TagFactory
