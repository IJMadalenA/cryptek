import logging

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django_ratelimit.decorators import ratelimit
from transformers import pipeline

from library_tomb.forms.comment_form import CommentForm
from library_tomb.models.entry import Entry

logger = logging.getLogger(__name__)

PERSPECTIVE_API_KEY = "your_api_key_here"
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

# Load the sentiment-analysis pipeline
moderation_pipeline = pipeline("sentiment-analysis")


def moderate_comment(content):
    """
    Moderate the comment content using a sentiment-analysis pipeline.

    Args:
        content (str): The content of the comment to be moderated.

    Returns:
        bool: True if the comment is not negative, False otherwise.
    """
    result = moderation_pipeline(content)
    return result[0]["label"] != "NEGATIVE"


@method_decorator(ratelimit(key="ip", rate="10/m"), name="dispatch")
class CommentCreateView(FormView):
    """
    View to handle the creation of comments.

    Attributes:
        form_class (CommentForm): The form class used to create a comment.
        template_name (str): The template used to render the form.
    """

    form_class = CommentForm
    template_name = "comment.html"

    def form_valid(self, form):
        """
        Handle a valid form submission.

        Args:
            form (CommentForm): The submitted form.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """
        if not self.request.user.is_authenticated:
            return JsonResponse(
                {"success": False, "message": "User not authenticated"}, status=403
            )
        entry = get_object_or_404(Entry, slug=self.kwargs["slug"], status=1)
        comment = form.save(commit=False)
        comment.entry = entry
        comment.user = self.request.user
        if moderate_comment(comment.content):
            comment.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Comment successfully added!",
                    "data": {
                        "id": comment.id,
                        "entry": comment.entry.title,
                        "user": self.request.user.username,
                        "content": comment.content,
                        "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    },
                },
                status=201,
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Comment not appropriate"}, status=400
            )

    def form_invalid(self, form):
        """
        Handle an invalid form submission.

        Args:
            form (CommentForm): The submitted form.

        Returns:
            JsonResponse: A JSON response indicating the form errors.
        """
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
