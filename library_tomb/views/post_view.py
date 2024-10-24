import logging

from django.views.generic import DetailView, ListView

from library_tomb.models.post import Post
from library_tomb.serializers.post_serializer import PostSerializerOut

logger = logging.getLogger(__name__)


class PostList(ListView):
    """
    Return all posts that are with status 1 (published) and order from the latest one.
    """

    queryset = (
        Post.objects.defer(
            "overview",
            "id",
            "slug",
            "created_at",
            "updated_at",
            "content",
            "author",
        )
        .filter(status=1)
        .order_by("-created_at")
    )
    template_name = "index.html"
    paginate_by = 3


class PostDetail(DetailView):
    """
    Retrieve a post by its slug.
    """

    queryset = Post.objects.defer(
        "overview",
        "id",
        "slug",
    ).filter(status=1)
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            del context["post"]
            del context["view"]
            serializer = PostSerializerOut(data=context["object"].__dict__)
            if serializer.is_valid():
                return context
            else:
                raise Exception
        except Exception as e:
            logger.error(e)
