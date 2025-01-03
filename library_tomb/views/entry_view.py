import logging

from django.views.generic import DetailView, ListView

from library_tomb.models.entry import Entry
from library_tomb.serializers.entry_serializer import EntrySerializerOut

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
    template_name = "index.html"
    paginate_by = 4


class EntryDetail(DetailView):
    """
    Retrieve a Entry by its slug.
    """

    queryset = Entry.objects.defer(
        "overview",
        "id",
        "slug",
    ).filter(status=1)
    template_name = "entry_detail.html"

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
