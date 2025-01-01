import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from message_app.forms.contact_me_form import ContactMeForm

logger = logging.getLogger(__name__)


class ContactMeView(View):
    def get(self, request):
        form = ContactMeForm(user=request.user)
        return render(request, "contact.html", {"form": form})

    def post(self, request):
        form = ContactMeForm(request.POST, user=request.user)

        if form.is_valid():
            name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")

            # Send email
            send_mail(
                subject=f"Contact Form Submission from {name} {last_name}",
                message=message,
                from_email=email,
                recipient_list=(settings.EMAIL_HOST_USER,),
            )
            return HttpResponseRedirect(reverse("contact_success"))

        return render(request, "contact.html", {"form": form})
