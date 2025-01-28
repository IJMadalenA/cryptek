from django import forms


class ContactMeForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Your Username",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    is_authenticated = forms.BooleanField(required=False, widget=forms.HiddenInput())
    first_name = forms.CharField(
        max_length=100,
        label="Your First Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,  # Default required for unauthenticated users
    )
    last_name = forms.CharField(
        max_length=100,
        label="Your Last Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,  # Default required for unauthenticated users
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True,  # Default required for unauthenticated users
    )
    message = forms.CharField(
        label="Your Message",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=True,
    )

    def __init__(self, *args, user=None, **kwargs):
        """
        Customize the fields based on whether the user is authenticated.

        Args:
            user: The request.user object to check user state.
        """
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields["is_authenticated"].initial = True
            self.fields["username"].widget = forms.HiddenInput()
            self.fields["first_name"].widget.attrs.update(
                {"readonly": True, "class": "form-control-plaintext"}
            )
            self.fields["first_name"].initial = user.first_name
            self.fields["first_name"].required = False
            self.fields["last_name"].widget.attrs.update(
                {"readonly": True, "class": "form-control-plaintext"}
            )
            self.fields["last_name"].initial = user.last_name
            self.fields["last_name"].required = False
            self.fields["email"].widget.attrs.update(
                {"readonly": True, "class": "form-control-plaintext"}
            )
            self.fields["email"].initial = user.email
            self.fields["email"].required = False
