from allauth.account.forms import SignupForm
from allauth.account.views import SignupView


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none",
                    "placeholder": field.label,
                }
            )

    def save(self, request):
        user = super().save(request)
        return user


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_message"] = "Welcome to the signup page!"
        return context
