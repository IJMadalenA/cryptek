from cryptek.test_and_check.base_model_test import BaseModelTestCase
from library_tomb.factories.category_factory import CategoryFactory
from library_tomb.factories.comment_factory import CommentFactory
from library_tomb.factories.entry_factory import EntryFactory
from library_tomb.factories.like_factory import LikeFactory
from library_tomb.factories.multimedia_factory import MultimediaFactory
from library_tomb.factories.tag_factory import TagFactory


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
