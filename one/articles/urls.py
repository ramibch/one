from django.urls import path

from .views import ArticleListView

urlpatterns = [
    # Article list
    path("", ArticleListView.as_view(), name="article_list"),
]
