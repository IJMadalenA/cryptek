from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from conscious_element.forms.contact_me_form import ContactForm


class ContactMeView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Send email
            send_mail(
                f'Contact Form Submission from {name}',
                message,
                email,
                ['your_email@example.com'],  # Replace with your recipient email
            )
            return HttpResponseRedirect(reverse('contact_success'))
        return render(request, 'contact.html', {'form': form})