import bleach
from django import forms


class ContactMeForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Your Username",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 bg-gray-100 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            }
        ),
        required=False,
    )
    is_authenticated = forms.BooleanField(required=False, widget=forms.HiddenInput())

    first_name = forms.CharField(
        max_length=100,
        label="Your First Name",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 bg-gray-100 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            }
        ),
        required=True,
    )

    last_name = forms.CharField(
        max_length=100,
        label="Your Last Name",
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-3 py-2 bg-gray-100 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            }
        ),
        required=True,
    )

    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-3 py-2 bg-gray-100 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            }
        ),
        required=True,
    )

    message = forms.CharField(
        label="Your Message",
        widget=forms.Textarea(
            attrs={
                "class": "w-full px-3 py-2 bg-gray-100 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 h-32 resize-none"
            }
        ),
        required=True,
    )

    def clean_message(self):
        """Avoid XSS attacks by cleaning the message field."""
        data = self.cleaned_data["message"]
        return bleach.clean(data)

    def __init__(self, *args, user=None, **kwargs):
        """Customize the fields based on whether the user is authenticated."""
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields["is_authenticated"].initial = True
            self.fields["username"].widget = forms.HiddenInput()

            self.fields["first_name"].widget.attrs.update(
                {
                    "readonly": True,
                }
            )
            self.fields["first_name"].initial = user.first_name
            self.fields["first_name"].required = False

            self.fields["last_name"].widget.attrs.update(
                {
                    "readonly": True,
                }
            )
            self.fields["last_name"].initial = user.last_name
            self.fields["last_name"].required = False

            self.fields["email"].widget.attrs.update(
                {
                    "readonly": True,
                }
            )
            self.fields["email"].initial = user.email
            self.fields["email"].required = False
