from django.views.generic import TemplateView


class ContactSuccessView(TemplateView):
    template_name = "contact_success.html"
