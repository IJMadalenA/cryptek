from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from library_tomb.models.entry import Entry
from django_ratelimit.decorators import ratelimit

@method_decorator(ratelimit(key="ip", rate="10/m"), name="dispatch")
class CommentCreateView(FormView):
    """

    """

    def port(self, request, *args, **kwargs):
        entry_id = kwargs.get(
            "entry_id",
        )
        user = request.user
        entry = get_object_or_404(
            Entry, id=entry_id, status=1
        )
        form = self.form_class(
            request.POST,
        )
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.user = user
            comment.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Comment successfully added!",
                    "data": {
                        "id": comment.id,
                        "entry": comment.entry.title,
                        "user": user.username,
                        "content": comment.content,
                        "created_at": comment.created_at,
                    },
                },
                status=201,
            )
        else:
            # Return validation errors as JSON
            return JsonResponse(
                {"success": False, "errors": form.errors}, status=400
            )
