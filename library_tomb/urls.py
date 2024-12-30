from django.urls import path
from django.views.generic import TemplateView

from message_app.views.contact_me_view import ContactMeView

from . import views
from .sitemaps import PostSitemap

sitemaps = {
    "post-detail": PostSitemap
}
urlpatterns = [
    path("", views.PostList.as_view(), name="main_page"),
    path("home/", views.PostList.as_view(), name="home"),
    path("contact/", ContactMeView.as_view(), name="contact"),
    path(
        "contact/success/",
        TemplateView.as_view(template_name="contact_success.html"),
        name="contact_success",
    ),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
]
