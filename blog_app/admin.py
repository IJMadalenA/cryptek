from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.decorators import action
from django.contrib.admin.options import ShowFacets

from blog_app.models.category import Category
from blog_app.models.comment import Comment
from blog_app.models.entry import Entry
from blog_app.models.like import Like
from blog_app.models.multimedia import Multimedia
from blog_app.models.tag import Tag


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        "entry",
        "parent",
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
class EntryAdmin(ModelAdmin):
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
        ("cdn_image_url", "cdn_image_public_id"),
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

    def get_readonly_fields(self, request, obj=None):
        """Allow superusers to edit 'author', but keep it readonly for others."""
        base_readonly_fields = ["slug", "created_at", "updated_at", "cdn_image_url", "cdn_image_public_id"]
        if request.user.is_superuser:
            return base_readonly_fields  # 'author' is editable
        return base_readonly_fields + ["author", "updated_at"]  # 'author' is readonly

    def save_model(self, request, obj, form, change):
        """Assign the author only if the entry is new and the user is not a superuser."""
        if not change and not request.user.is_superuser:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@register(Tag)
class TagAdmin(ModelAdmin):
    pass
