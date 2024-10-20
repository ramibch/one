from django.urls import path

from .views import ArticleDetailView, ArticleListView

urlpatterns = [
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("", ArticleListView.as_view(), name="article-list"),
]
