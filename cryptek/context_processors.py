from cryptek.ai_system.gemini_tip import get_gemini_tip


def gemini_tip_context(request):
    return {"tip": get_gemini_tip()}
