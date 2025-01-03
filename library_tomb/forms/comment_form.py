from django.forms.models import ModelForm

from library_tomb.models.comment import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = (
            "content",
        )