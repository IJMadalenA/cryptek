from django.urls import path

from . import views
from .sitemaps import EntrySitemap
from .views.like_view import LikeView
from .views.terms_and_privacy_view import PrivacyPolicyView, TermsOfServiceView

sitemaps = {"entry-detail": EntrySitemap}
app_name = "blog_app"

urlpatterns = [
    path(route="", view=views.EntryList.as_view(), name="main_page"),
    path(route="home/", view=views.EntryList.as_view(), name="home"),
    path(route="entry/<slug:slug>/", view=views.EntryDetail.as_view(), name="entry_detail"),
    path(route="entry/like/<slug:slug>", view=LikeView.as_view(), name="like_entry"),
    path(route="privacy-policy/", view=PrivacyPolicyView.as_view(), name="privacy_policy"),
    path(route="terms-of-service/", view=TermsOfServiceView.as_view(), name="terms_of_service"),
]
