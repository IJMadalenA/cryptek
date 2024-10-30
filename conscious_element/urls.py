from django.urls import path

from conscious_element.views.session_view import (SessionDeleteOtherView,
                                                  SessionDeleteView,
                                                  SessionListView)

urlpatterns = [
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
