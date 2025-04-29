from blog_app.models.comment import Comment
from django.forms.models import ModelForm
from django.forms.widgets import Textarea


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
