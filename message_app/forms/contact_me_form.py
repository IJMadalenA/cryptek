from django import forms


class ContactMeForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Your Username",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    is_authenticated = forms.BooleanField(required=False, widget=forms.HiddenInput())
    first_name = forms.CharField(
        max_length=100,
        label="Your First Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=100,
        label="Your Surname",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Your Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(
        label="Your Message", widget=forms.Textarea(attrs={"class": "form-control"})
    )
