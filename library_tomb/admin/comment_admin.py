from django.contrib.admin import ModelAdmin, register

from library_tomb.models.comment import Comment


@register(Comment)
class CommentAdmin(ModelAdmin):
    pass
