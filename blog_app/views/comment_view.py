# views/comment_view.py
import ast

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from blog_app.forms.comment_form import CommentForm
from blog_app.models.comment import Comment
from blog_app.models.entry import Entry


# from cryptek.ai_system.comment_moderation import CommentModeration


class CommentView(View, FormMixin, SingleObjectMixin):
    """
    A view for handling comments on entries. This view supports various HTTP methods
    such as GET, POST, PUT, and DELETE to manage comments.

    Inherits from:
        - View: Base class for all views in Django.
        - FormMixin: Provides a way to handle forms in class-based views.
        - SingleObjectMixin: Provides a way to handle a single object for the view.

    Attributes:
        model (Comment): The model associated with this view.
        form_class (CommentForm): The form class used for creating and updating comments.
        template_name (str): The template used to render the view.
    """

    model = Comment
    form_class = CommentForm
    template_name = "entry_detail.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.moderation = CommentModeration()

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)

        content = form.cleaned_data.get("content")
        # acceptable, label = self.moderation.moderate_comment(content)

        # if not acceptable:
        #     return JsonResponse({"success": False, "message": f"Comment not acceptable: {label}"}, status=400)

        entry = get_object_or_404(Entry, slug=self.kwargs["slug"], status=1)
        comment = form.save(commit=False)
        comment.entry = entry
        comment.user = self.request.user
        comment.save()
        return JsonResponse({"success": True, "message": "Comment successfully added!"}, status=201)

    def form_invalid(self, form):
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def get(self, *args, **kwargs):
        entry = get_object_or_404(Entry, slug=self.kwargs["slug"], status=1)
        comments = entry.comments.all()
        return JsonResponse(data={"success": True, "comments": list(comments.values())}, status=200)

    @method_decorator(login_required(login_url="/accounts/login/"))
    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    @method_decorator(login_required(login_url="/accounts/login/"))
    def put(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)

        comment = kwargs.get("pk", None)
        if not comment or not isinstance(comment, int):
            return JsonResponse({"success": False, "message": "Comment ID not provided"}, status=400)

        comment = get_object_or_404(Comment, id=comment)
        if (self.request.user != comment.user) and not (self.request.user.is_staff or self.request.user.is_superuser):
            return HttpResponseForbidden("You do not have permission to edit this comment.")

        # https://docs.python.org/3/library/ast.html
        content = ast.literal_eval(self.request.body.decode("utf-8"))
        content = content.get("content", None)

        if not content or not isinstance(content, str):
            return JsonResponse(
                {"success": False, "message": "Error - Content not provided or is not a string"}, status=400
            )
        # acceptable, label = self.moderation.moderate_comment(content)
        # if not acceptable:
        #     return JsonResponse({"success": False, "message": f"Comment not acceptable: {label}"}, status=400)

        # Django forms only work with GET and POST methods. That's the reason why we can't implement forms here.
        comment.content = content
        comment.save()

        return JsonResponse({"success": True, "message": "Comment successfully updated!"}, status=200)

    @method_decorator(login_required(login_url="/accounts/login/"))
    def delete(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)
        comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        if self.request.user != comment.user and not self.request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to delete this comment.")
        comment.delete()
        return JsonResponse({"success": True, "message": "Comment successfully deleted!"}, status=200)
