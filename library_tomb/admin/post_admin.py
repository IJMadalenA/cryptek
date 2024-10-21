from django.contrib.admin import register, ModelAdmin

from library_tomb.models.post import Post


@register(Post)
class PostAdmin(ModelAdmin):
    pass
