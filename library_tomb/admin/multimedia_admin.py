from django.contrib.admin import ModelAdmin, register

from library_tomb.models.multimedia import Multimedia


@register(Multimedia)
class MultimediaAdmin(ModelAdmin):
    pass
