from django.forms.models import ModelForm
from django.forms.widgets import Textarea

from library_tomb.models.comment import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Comment here...",
                    "rows": 3,
                }
            )
        }
        labels = {
            "content": "",
        }
