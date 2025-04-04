from django.db.models import CharField, Model


# Tag model
class Tag(Model):
    name = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
