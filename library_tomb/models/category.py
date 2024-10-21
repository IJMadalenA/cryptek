# Category model
from django.db.models import Model, CharField, TextField, SlugField, ImageField


class Category(Model):
    name = CharField(max_length=100, unique=True)
    subtitle = CharField(max_length=20)
    description = TextField(blank=True)
    slug = SlugField()
    thumbnail = ImageField()


    def str(self):
        return self.name
