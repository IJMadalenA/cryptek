from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"


class TermsOfServiceView(TemplateView):
    template_name = "terms_of_service.html"
