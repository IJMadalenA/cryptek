from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from blog_app.models.entry import Entry
from blog_app.models.like import Like


class LikeView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "User not authenticated"}, status=403)

        entry = get_object_or_404(Entry, slug=self.kwargs["slug"])
        like_type = request.POST.get("type", Like.LIKE)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        ip_address = request.META.get("REMOTE_ADDR", "")

        like, created = Like.objects.update_or_create(
            entry=entry,
            user=request.user,
            defaults={
                "type": like_type,
                "user_agent": user_agent,
                "ip_address": ip_address,
            },
        )

        if created:
            message = f"{like_type.capitalize()} added successfully!"
        else:
            message = f"{like_type.capitalize()} updated successfully!"

        return JsonResponse({"success": True, "message": message}, status=201)
