from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from conscious_element.forms.create_account_form import CreateAccountForm


class CreateAccountView(FormView):
    template_name = "create_account.html"
    form_class = CreateAccountForm
    success_url = reverse_lazy("home")  # Redirect to homepage after success

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Your account has been created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
