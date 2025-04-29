# user_app/views/profile_view.py
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from user_app.forms.profile_form import CustomPasswordChangeForm, ProfileForm, UserProfileForm


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = CustomPasswordChangeForm(request.user)

    return render(
        request, "profile.html", {"user_form": user_form, "profile_form": profile_form, "password_form": password_form}
    )
