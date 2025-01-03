from django.urls import path

from conscious_element.views.create_account_view import CreateAccountView
from conscious_element.views.session_view import (SessionDeleteOtherView,
                                                  SessionDeleteView,
                                                  SessionListView)

urlpatterns = [
    path(
        "create/",
        view=CreateAccountView.as_view(),
        name="create_account",
    ),
    path(
        "sessions/",
        view=SessionListView.as_view(),
        name="session_list",
    ),
    path(
        "sessions/other/delete/",
        view=SessionDeleteOtherView.as_view(),
        name="session_delete_other",
    ),
    path(
        "sessions/<str:pk>/delete/",
        view=SessionDeleteView.as_view(),
        name="session_delete",
    ),
]
