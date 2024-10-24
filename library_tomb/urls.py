from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("search/", views.PostListView.as_view(), name="post_search"),
    path("<int:pk>/", views.PostDetail.as_view(), name="post_detail"),
]
