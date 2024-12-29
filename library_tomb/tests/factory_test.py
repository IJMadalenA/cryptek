from cryptek.qa_templates import BaseFactoryTest
from library_tomb.factories.category_factory import CategoryFactory
from library_tomb.factories.comment_factory import CommentFactory
from library_tomb.factories.like_factory import LikeFactory
from library_tomb.factories.multimedia_factory import MultimediaFactory
from library_tomb.factories.post_factory import PostFactory
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
    class Meta:
        factory = PostFactory


class TagFactoryTestCase(BaseFactoryTest):
    class Meta:
        factory = TagFactory
