import threading

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView

from blog_app.utils.token_generator import EmailConfirmationTokenGenerator
from conscious_element.forms.create_account_form import CreateAccountForm


# --- Asynchronous function ---
def send_email_in_background(subject, html_content, from_email, to_email):
    def send_async():
        msg = EmailMultiAlternatives(subject, "", from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    threading.Thread(target=send_async).start()


class CreateAccountView(FormView):
    template_name = "create_account.html"
    form_class = CreateAccountForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        token_generator = EmailConfirmationTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(
            reverse("verify_email", kwargs={"uidb64": uidb64, "token": token})
        )
        subject = "Verify your email"
        html_content = f"<p>Click the link to verify your email: " f'<a href="{verify_url}">Verify</a></p>'
        send_email_in_background(subject, html_content, "noreply@example.com", [user.email])
        login(self.request, user)
        messages.success(self.request, "Your account has been created successfully!")
        return super().form_valid(form)


# --- Email Confirmation View with user feedback ---
class EmailConfirmationView(View):
    def get(self, request, uidb64, token):
        from django.contrib import messages

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except:
            messages.error(request, "Invalid email verification link.")
            return redirect("home")

        token_generator = EmailConfirmationTokenGenerator()
        if token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            messages.success(request, "Email confirmed successfully.")
        else:
            messages.error(request, "The link is invalid or expired.")
        return redirect("home")
