from blog_app.models.code_tip import CodeTip
from django.shortcuts import render


def gemini_tip_box(request):
    tip = CodeTip.generate_code_tip()
    return render(request, "gemini_tip_box.html", {"tip": tip})
