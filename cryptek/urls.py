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
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView

from blog_app.sitemaps import EntrySitemap
from blog_app.views import CommentView
from blog_app.views.email_verification_view import EmailConfirmationView
from conscious_element.views.about_me import about_me
from conscious_element.views.login_view import CustomLoginView
from conscious_element.views.singup_view import CustomSignupView
from cryptek.csp_report_view import csp_report_view
from message_app.views.contact_me_view import ContactMeView

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
        path("account/", include("conscious_element.urls")),
        path("blog/", include("blog_app.urls"), name="blog"),
        path("contact/", ContactMeView.as_view(), name="contact"),
        path(
            "entry/<slug:slug>/comment/<int:pk>/",
            CommentView.as_view(),
            name="put_delete_comment",
        ),
        path("entry/<slug:slug>/comment/", CommentView.as_view(), name="get_post_comment"),
        path("accounts/login/", CustomLoginView.as_view(), name="login"),
        path("accounts/signup/", CustomSignupView.as_view(), name="signup"),
        path("logout/", LogoutView.as_view(), name="logout"),
        path(
            "verify-email/<uidb64>/<token>/",
            EmailConfirmationView.as_view(),
            name="verify_email",
        ),
    ]
    + third_party_apps_urls
    + debug_toolbar_urls()
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
