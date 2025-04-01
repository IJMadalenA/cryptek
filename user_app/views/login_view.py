from allauth.account.forms import LoginForm
from allauth.account.views import LoginView as AllAuthLoginView
from django.contrib import messages
from django.urls import reverse_lazy


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Enter your username or email",
                "class": "form-control",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Enter your password",
                "class": "form-control",
            }
        )


class CustomLoginView(AllAuthLoginView):
    authentication_form = CustomLoginForm
    success_url = reverse_lazy("main_page")
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"You are now logged.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
