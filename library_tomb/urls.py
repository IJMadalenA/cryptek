from django.urls import path

from message_app.views.contact_me_view import ContactMeView
from message_app.views.contact_success_view import ContactSuccessView

from . import views
from .sitemaps import EntrySitemap

sitemaps = {"entry-detail": EntrySitemap}
urlpatterns = [
    path("", views.EntryList.as_view(), name="main_page"),
    path("home/", views.EntryList.as_view(), name="home"),
    path("contact/", ContactMeView.as_view(), name="contact"),
    path(
        "contact/success/",
        ContactSuccessView.as_view(),
        name="contact_success",
    ),
    path("<slug:slug>/", views.EntryDetail.as_view(), name="entry_detail"),
]
