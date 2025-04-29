from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from blog_app.models.code_tip import CodeTip


def code_tip_box(request):
    return render(request, "code_tip_box.html")


@require_GET
def code_tip_api(request):
    from django.core.cache import cache

    tip = cache.get("gemini_tip")
    if not tip:
        tip = CodeTip.generate_code_tip()
        cache.set("gemini_tip", tip, timeout=60 * 10)
    return JsonResponse(tip)
