from django.contrib.auth.views import LogoutView


class CustomLogoutView(LogoutView):
    next_page = "login/"
