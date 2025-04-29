from blog_app.utils.token_generator import EmailConfirmationTokenGenerator
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

User = get_user_model()
email_token = EmailConfirmationTokenGenerator()


class EmailConfirmationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return HttpResponse("Invalid link.")

        if email_token.check_token(user, token):
            user.email_verified = True
            user.save()
            return HttpResponse("Email confirmed successfully.")
        return HttpResponse("Invalid or expired link.")
