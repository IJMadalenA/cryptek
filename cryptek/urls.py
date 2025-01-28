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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView

from conscious_element.views.about_me import about_me
from conscious_element.views.login_view import CustomLoginView
from cryptek.csp_report_view import csp_report_view
from library_tomb.sitemaps import EntrySitemap
from message_app.views.contact_me_view import ContactMeView

sitemaps = {
    "entries": EntrySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("conscious_element.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("", RedirectView.as_view(url='blog/', permanent=True)),
    path("", RedirectView.as_view(url="blog", permanent=True), name="to_blog"),
    path("blog/", include("library_tomb.urls"), name="blog"),
    path("markdownx/", include("markdownx.urls")),
    path("about/", about_me, name="about_me"),
    path("contact/", ContactMeView.as_view(), name="contact"),
    path("csp-violations/", csp_report_view, name="csp_report_view"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
