from django.urls import path

from user_app.views.session_view import SessionDeleteOtherView, SessionDeleteView, SessionListView
from user_app.views.user_profile_view import PublicProfileView, personal_profile_view, update_profile_view

urlpatterns = [
    path(
        route="sessions/",
        view=SessionListView.as_view(),
        name="session_list",
    ),
    path(
        route="sessions/other/delete/",
        view=SessionDeleteOtherView.as_view(),
        name="session_delete_other",
    ),
    path(
        route="sessions/<str:pk>/delete/",
        view=SessionDeleteView.as_view(),
        name="session_delete",
    ),
    path(route="profile/<str:username>/", view=PublicProfileView.as_view(), name="public_profile"),
    path(route="profile/", view=personal_profile_view, name="personal_profile"),
    path(route="profile/edit/", view=update_profile_view, name="edit_profile"),
]
