from django.urls import path

from message_app.views.contact_success_view import ContactSuccessView
from . import views
from .sitemaps import EntrySitemap
from .views import CommentView

sitemaps = {"entry-detail": EntrySitemap}
urlpatterns = [
    path("", views.EntryList.as_view(), name="main_page"),
    path("home/", views.EntryList.as_view(), name="home"),
    path("entry/<slug:slug>/", views.EntryDetail.as_view(), name="entry_detail"),
    path("<slug:slug>/", views.EntryDetail.as_view(), name="entry_detail"),
    path("entry/<slug:slug>/comment/", CommentView.as_view(), name="get_post_comment"),
    path(
        "entry(<slug:slug>)/comment/<int:pk>",
        CommentView.as_view(),
        name="put_delete_comment",
    ),
    path(
        "contact/success/",
        ContactSuccessView.as_view(),
        name="contact_success",
    ),
]
