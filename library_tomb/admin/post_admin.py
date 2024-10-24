from django.contrib.admin import ShowFacets, register
from markdownx.admin import MarkdownxModelAdmin

from library_tomb.models.post import Post


@register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = (
        "title",
        "status",
        "featured",
        "created_at",
        "updated_at",
    )
    fields = (
        "title",
        "header_image",
        "content",
        "overview",
        ("categories", "tags"),
        ("status", "featured"),
        "slug",
        (
            "created_at",
            "updated_at",
        ),
    )
    search_fields = (
        "title",
        "categories__name",
        "tags__name",
    )
    show_facets = ShowFacets.ALWAYS
    readonly_fields = ("slug", "created_at", "updated_at")
