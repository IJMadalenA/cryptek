from django.shortcuts import render

from cryptek.ai_system.gemini_tip import get_gemini_tip


def gemini_tip_box(request):
    tip = get_gemini_tip()
    return render(request, "gemini_tip_box.html", {"tip": tip})
