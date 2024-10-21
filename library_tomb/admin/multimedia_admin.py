from django.contrib.admin import register, ModelAdmin

from library_tomb.models.multimedia import Multimedia


@register(Multimedia)
class MultimediaAdmin(ModelAdmin):
    pass
