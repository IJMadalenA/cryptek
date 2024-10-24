from rest_framework.fields import CharField, DateTimeField, ImageField
from rest_framework.serializers import ModelSerializer

from library_tomb.models.post import Post


class PostSerializerOut(ModelSerializer):
    title = CharField(read_only=True)
    content = CharField(read_only=True)
    author = CharField(
        read_only=True,
        source="author.username",
    )
    created_at = DateTimeField(
        read_only=True,
        format="%Y-%m-%d",
    )
    header_image = ImageField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "author",
            "created_at",
            "updated_at",
            "header_image",
        )
