from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django_ratelimit.decorators import ratelimit

from library_tomb.forms.comment_form import CommentForm
from library_tomb.models.comment import Comment
from library_tomb.models.entry import Entry


@method_decorator(ratelimit(key="ip", rate="10/m"), name="dispatch")
class CommentView(View, FormMixin, SingleObjectMixin):
    model = Comment
    form_class = CommentForm
    template_name = "entry_detail.html"

    def get(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, slug=self.kwargs["slug"], status=1)
        comments = entry.comments.all()
        return JsonResponse({"success": True, "comments": list(comments.values())}, status=200)

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)
        entry = get_object_or_404(Entry, slug=self.kwargs["slug"], status=1)
        comment = form.save(commit=False)
        comment.entry = entry
        comment.user = self.request.user
        comment.save()
        return JsonResponse({"success": True, "message": "Comment successfully added!"}, status=201)

    def form_invalid(self, form):
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)
        entry = get_object_or_404(Entry, slug=self.kwargs["slug"], status=1)
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.user = request.user
            comment.save()
            return JsonResponse({"success": True, "message": "Comment successfully added!"}, status=201)
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)
        comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        if request.user != comment.user and not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to edit this comment.")
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Comment successfully updated!"}, status=200)
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)
        comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        if request.user != comment.user and not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to delete this comment.")
        comment.delete()
        return JsonResponse({"success": True, "message": "Comment successfully deleted!"}, status=200)
