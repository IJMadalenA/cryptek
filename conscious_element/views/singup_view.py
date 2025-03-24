from allauth.account.forms import SignupForm
from allauth.account.views import SignupView


class MyCustomSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        return user


class CustomSignupView(SignupView):
    form_class = MyCustomSignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_message"] = "Welcome to the signup page!"
        return context
