"""
URL configuration for cryptek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from allauth.account.views import LogoutView
from blog_app.sitemaps import EntrySitemap
from blog_app.views.code_tip_view import code_tip_api
from blog_app.views.email_verification_view import EmailConfirmationView
from cryptek.csp_report_view import csp_report_view
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView
from message_app.views.contact_me_view import ContactMeView
from user_app.views.about_me import about_me
from user_app.views.login_view import CustomLoginView
from user_app.views.singup_view import CustomSignupView

sitemaps = {
    "entries": EntrySitemap,
}

third_party_apps_urls = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("markdownx/", include("markdownx.urls")),
    path("csp-violations/", csp_report_view, name="csp_report_view"),
    path("accounts/", include("allauth.urls")),
]

urlpatterns = (
    [
        path("", RedirectView.as_view(url="blog", permanent=True), name="to_blog"),
        path("about/", about_me, name="about_me"),
        path("admin/", admin.site.urls),
        path("account/", include("user_app.urls")),
        path("blog/", include("blog_app.urls"), name="blog"),
        path("contact/", ContactMeView.as_view(), name="contact"),
        path("accounts/login/", CustomLoginView.as_view(), name="login"),
        path("accounts/signup/", CustomSignupView.as_view(), name="signup"),
        path("logout/", LogoutView.as_view(), name="logout"),
        path(
            "verify-email/<uidb64>/<token>/",
            EmailConfirmationView.as_view(),
            name="verify_email",
        ),
        path("api/code-tip/", code_tip_api, name="code_tip_api"),
    ]
    + third_party_apps_urls
    + debug_toolbar_urls()
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
