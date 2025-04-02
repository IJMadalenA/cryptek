from django.urls import path

from user_app.views.session_view import SessionDeleteOtherView, SessionDeleteView, SessionListView

urlpatterns = [
    path(
        route="profile/",
        view=SessionListView.as_view(),
        name="profile",
    ),
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
]
