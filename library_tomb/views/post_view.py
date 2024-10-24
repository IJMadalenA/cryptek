from django.views.generic import ListView, DetailView

from library_tomb.models.post import Post


class PostList(ListView):
    """
    Return all posts that are with status 1 (published) and order from the latest one.
    """

    queryset = Post.objects.filter(status=1).order_by("-created_at")
    template_name = "index.html"
    paginate_by = 3


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
