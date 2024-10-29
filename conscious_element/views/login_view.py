from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy("blog/")
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request, f'You are now logged in as {form.cleaned_data["username"]}.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
