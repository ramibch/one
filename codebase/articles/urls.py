
from django.urls import path

from .views import ArticleDetailView

urlpatterns = [
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
]
