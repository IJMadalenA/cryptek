import random

from django.core.cache import cache

from blog_app.models.code_tip import CodeTip


def gemini_tip_context(request):
    exclude_prefixes = ["/admin/", "/static/", "/media/", "/login/", "/logout/", "/register/"]
    if any(request.path.startswith(prefix) for prefix in exclude_prefixes):
        return {}
    # Intenta obtener el tip de la caché
    tip = cache.get("gemini_tip")
    if not tip:
        try:
            tip = CodeTip.generate_code_tip()
            # Si hay error en la generación, intenta obtener uno aleatorio
            if not tip or tip.get("error_message"):
                raise Exception("Error al generar tip")
            cache.set("gemini_tip", tip, timeout=60 * 10)
        except Exception:
            # Si no se puede generar, usa uno aleatorio existente
            tips = list(CodeTip.objects.all())
            if tips:
                tip_obj = random.choice(tips)
                tip = {
                    "title": tip_obj.title,
                    "description": tip_obj.description,
                    "code": tip_obj.code,
                }
            else:
                tip = {
                    "title": "No hay tips disponibles",
                    "description": "No se pudo obtener un tip de código en este momento.",
                    "code": "",
                }
    return {"tip": tip}
