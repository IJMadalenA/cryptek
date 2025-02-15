from cryptek.test_and_check.base_factory_test import BaseFactoryTest
from library_tomb.factories.category_factory import CategoryFactory
from library_tomb.factories.comment_factory import CommentFactory
from library_tomb.factories.entry_factory import (
    EntryAnalyticsFactory,
    EntryFactory,
    EntryReactionFactory,
    EntryVersionFactory,
)
from library_tomb.factories.like_factory import LikeFactory
from library_tomb.factories.multimedia_factory import MultimediaFactory
from library_tomb.factories.tag_factory import TagFactory


class CategoryFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = CategoryFactory


class CommentFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = CommentFactory


class LikeFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = LikeFactory


class MultimediaFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = MultimediaFactory


class PostFactoryTestCase(BaseFactoryTest):

    def test_get_absolute_url_method(self):
        entry = EntryFactory(
            title="Test Entry Title"
        )  # Pass a title for slug generation
        expected_url = f"/blog/{entry.slug}/"
        self.assertEqual(entry.get_absolute_url(), expected_url)

    class Meta:
        factory = EntryFactory


class PostVersionFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = EntryVersionFactory


class PostReactionFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = EntryReactionFactory


class PostAnalyticsFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = EntryAnalyticsFactory


class TagFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = TagFactory
