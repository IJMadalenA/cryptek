from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from rest_framework import permissions

from user_app.forms.profile_form import ProfileUpdateForm
from user_app.models.profile import Profile


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allows only the owner to edit the profile, but allows others to read it."""

    def has_object_permission(self, request, view, obj):
        # Enables GET, HEAD, OPTIONS for all.
        if request.method in permissions.SAFE_METHODS:
            return obj.visibility == Profile.Visibility.PUBLIC or obj.user == request.user

        # Only allows changes to the profile owner.
        return obj.user == request.user


class PublicProfileView(View):
    """Public view of the user profile."""

    def get(self, request, username):
        profile = get_object_or_404(Profile, user__username=username)

        # If the profile is private and the user is not the owner, redirect.
        if profile.visibility == Profile.Visibility.PRIVATE and profile.user != request.user:
            messages.warning(request, "Este perfil es privado.")
            return redirect("user_app:personal_profile")

        return render(request, "public_profile.html", {"profile": profile})


@login_required
def personal_profile_view(request):
    """Authenticated user profile view."""
    profile = request.user.profile
    return render(request, "personal_profile.html", {"profile": profile})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View to update the authenticated user's profile."""

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "update_profile.html"
    success_url = reverse_lazy("user_app:personal_profile")

    def get_object(self, queryset=None):
        """Ensures the user can only edit their own profile."""
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        """Adds a success message when the profile is updated."""
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)
