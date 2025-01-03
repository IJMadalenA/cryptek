from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.decorators import action
from django.contrib.admin.options import ShowFacets
from markdownx.admin import MarkdownxModelAdmin

from library_tomb.models.category import Category
from library_tomb.models.comment import Comment
from library_tomb.models.entry import Entry
from library_tomb.models.like import Like
from library_tomb.models.multimedia import Multimedia
from library_tomb.models.tag import Tag


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        "entry",
        "user",
        "content",
        "created_at",
        "updated_at",
        "active",
    )
    list_filter = ("active", "created_at")
    search_fields = (
        "entry__title",
        "user__username",
    )

    @action(description="Approve Comments")
    def approve_comments(self, queryset):
        queryset.update(active=True)


@register(Like)
class LikeAdmin(ModelAdmin):
    pass


@register(Multimedia)
class MultimediaAdmin(ModelAdmin):
    pass

@register(Entry)
class EntryAdmin(MarkdownxModelAdmin):
    list_display = (
        "title",
        "status",
        "featured",
        "created_at",
        "updated_at",
    )
    fields = (
        "title",
        "author",
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
    readonly_fields = ("author", "slug", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@register(Tag)
class TagAdmin(ModelAdmin):
    pass
