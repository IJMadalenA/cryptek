from django.db.models import Q
from django.views.generic import ListView
from django_filters import rest_framework as filters

from blog_app.models.entry import Entry


class PostFilter(filters.FilterSet):
    q = filters.CharFilter(method="filter_by_all", label="Search")

    class Meta:
        model = Entry
        fields = []

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(overview__icontains=value)).distinct()


class PostListView(ListView):
    model = Entry
    template_name = "search_bar.html"
    context_object_name = "object_list"
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context
