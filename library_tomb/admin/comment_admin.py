from django.contrib.admin import register, ModelAdmin

from library_tomb.models.comment import Comment


@register(Comment)
class CommentAdmin(ModelAdmin):
    pass
