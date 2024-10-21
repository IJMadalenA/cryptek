from django.db.models import Model, CharField


# Tag model
class Tag(Model):
    name = CharField(max_length=100, unique=True)

    def str(self):
        return self.name