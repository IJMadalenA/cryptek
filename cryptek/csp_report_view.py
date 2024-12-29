import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configura un logger específico para CSP
csp_logger = logging.getLogger("django_csp")


@csrf_exempt  # Los navegadores no envían CSRF tokens con los reportes de CSP
def csp_report_view(request):
    if request.method == "POST":
        try:
            # Parsear el contenido del reporte
            report_data = json.loads(request.body.decode("utf-8"))
            csp_logger.warning(f"CSP Violation: {json.dumps(report_data)}")
        except (ValueError, KeyError) as e:
            csp_logger.error(f"Error processing report CSP: {e}")
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "method not allowed"}, status=405)
