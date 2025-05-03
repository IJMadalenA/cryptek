from django.contrib.admin import ModelAdmin, register
from django.contrib.admin.decorators import action
from django.contrib.admin.options import ShowFacets
from django.utils.html import format_html

from blog_app.models import CodeTip
from blog_app.models.category import Category
from blog_app.models.comment import Comment
from blog_app.models.entry import Entry
from blog_app.models.gemini_api_usage import GeminiApiUsage
from blog_app.models.like import Like
from blog_app.models.multimedia import Multimedia
from blog_app.models.tag import Tag


@register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@register(CodeTip)
class CodeTipAdmin(ModelAdmin):
    list_display = ("title", "tech_stack", "level", "type_of_tip", "created_at", "has_error")
    list_filter = ("tech_stack", "level", "type_of_tip", "created_at")
    search_fields = ("title", "description", "code", "error_message")
    readonly_fields = ("created_at", "updated_at", "prompt_used", "gemini_raw_response", "error_message")
    fieldsets = (
        ("Basic Information", {"fields": ("title", "description", "code", "tech_stack", "level", "type_of_tip")}),
        (
            "Gemini API Details",
            {
                "fields": ("prompt_used", "gemini_raw_response", "error_message"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def has_error(self, obj):
        if obj.error_message:
            return format_html('<span style="color: red;">✘</span>')
        return format_html('<span style="color: green;">✓</span>')

    has_error.short_description = "Status"


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


@register(GeminiApiUsage)
class GeminiApiUsageAdmin(ModelAdmin):
    list_display = (
        "date",
        "model_name",
        "request_count",
        "successful_requests",
        "failed_requests",
        "tokens_used",
        "average_response_time",
        "success_rate",
        "has_errors",
    )
    list_filter = ("date", "model_name")
    readonly_fields = (
        "date",
        "request_count",
        "successful_requests",
        "failed_requests",
        "tokens_used",
        "average_response_time",
        "model_name",
        "last_error_message",
        "last_updated",
        "success_rate",
    )

    fieldsets = (
        (
            "Usage Statistics",
            {
                "fields": (
                    "date",
                    "model_name",
                    "request_count",
                    "successful_requests",
                    "failed_requests",
                    "tokens_used",
                    "average_response_time",
                    "success_rate",
                )
            },
        ),
        (
            "Error Information",
            {
                "fields": ("last_error_message", "last_updated"),
                "classes": ("collapse",),
            },
        ),
    )

    def success_rate(self, obj):
        if obj.request_count == 0:
            return "N/A"
        success_rate = (obj.successful_requests / obj.request_count) * 100
        color = "green" if success_rate > 90 else "orange" if success_rate > 70 else "red"
        formatted_rate = f"{success_rate:.1f}%"
        return format_html('<span style="color: {};">{}</span>', color, formatted_rate)

    def has_errors(self, obj):
        if obj.failed_requests > 0:
            return format_html('<span style="color: red;">✘</span>')
        return format_html('<span style="color: green;">✓</span>')

    success_rate.short_description = "Success Rate"
    has_errors.short_description = "Errors"

    def has_add_permission(self, request):
        # Prevent manual creation of usage records
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow deletion only for superusers
        return request.user.is_superuser
