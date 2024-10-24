from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("search/", views.PostListView.as_view(), name="post_search"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
]
