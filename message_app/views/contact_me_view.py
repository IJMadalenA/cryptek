import logging

from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from conscious_element.models.cryptek_user import CryptekUser
from message_app.forms.contact_me_form import ContactMeForm

logger = logging.getLogger(__name__)


class ContactMeView(View):
    def get(self, request):
        return render(request, "contact.html", {"form": ContactMeForm()})

    def post(self, request):
        try:
            form = ContactMeForm(request.POST)

            if request.user.is_authenticated:
                form.fields["username"].initial = request.user.username
                form.fields["first_name"].initial = request.user.first_name
                form.last_name["last_name"].initial = request.user.last_name
                form.fields["email"].initial = request.user.email
                form.fields["is_authenticated"].initial = True
            else:
                form.fields["username"].initial = "Anonymous"
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                form.fields["is_authenticated"].initial = False

                CryptekUser.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )

            if form.is_valid():
                name = form.cleaned_data["name"]
                message = form.cleaned_data["message"]
                # Send email
                send_mail(
                    f"Contact Form Submission from {name}",
                    message,
                    ["your_email@example.com"],  # Replace with your recipient email
                )
                return HttpResponseRedirect(reverse("contact_success"))
            return render(request, "contact.html", {"form": form})

        except Exception as e:
            logger.exception(e)
