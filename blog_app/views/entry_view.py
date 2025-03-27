import logging

from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from blog_app.forms.comment_form import CommentForm
from blog_app.models.entry import Entry
from blog_app.serializers.entry_serializer import EntrySerializerOut

logger = logging.getLogger(__name__)


class EntryList(ListView):
    """
    Return all entries that are with status 1 (published) and order from the latest one.
    """

    queryset = (
        Entry.objects.defer(
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
    template_name = "home.html"
    paginate_by = 4


class EntryDetail(FormMixin, DetailView):
    """
    Retrieve an Entry by its slug.
    """

    model = Entry
    template_name = "entry_detail.html"
    form_class = CommentForm
    queryset = Entry.objects.defer(
        "overview",
        "id",
        "slug",
    ).filter(status=1)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            del context["entry"]
            del context["view"]
            serializer = EntrySerializerOut(data=context["object"].__dict__)
            if serializer.is_valid():
                return context
            else:
                raise Exception
        except Exception as e:
            logger.error(e)
