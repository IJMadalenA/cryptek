from django.urls import path

from conscious_element.views.create_account_view import CreateAccountView
from conscious_element.views.session_view import (SessionDeleteOtherView,
                                                  SessionDeleteView,
                                                  SessionListView)

urlpatterns = [
    path(
        route="create/",
        view=CreateAccountView.as_view(),
        name="create_account",
    ),
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
