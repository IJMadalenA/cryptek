from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to="category_thumbnails/", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
