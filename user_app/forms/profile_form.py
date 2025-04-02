from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from user_app.models.profile import Profile


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date", "profile_picture", "visibility"]


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]


def validate_image(file):
    """Validate that the uploaded image is an allowed file and of adequate size."""
    valid_extensions = ["jpg", "jpeg", "png", "webp"]
    max_size = 2 * 1024 * 1024  # 2MB

    ext = file.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only JPG, PNG or WEBP image files are allowed.")

    if file.size > max_size:
        raise ValidationError("The image must not exceed 2MB.")


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, validators=[validate_image])

    class Meta:
        model = Profile
        fields = ["bio", "profile_picture", "location", "birth_date", "website", "phone_number", "visibility"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+1234567890"}),
            "website": forms.URLInput(attrs={"placeholder": "https://example.com"}),
            "visibility": forms.Select(choices=Profile.Visibility.choices),
        }
