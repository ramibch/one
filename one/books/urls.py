from django.urls import path

from .views import BookDetailView, BookListView

urlpatterns = [
    path("<slug:slug>/", BookDetailView.as_view(), name="book_detail"),
    path("", BookListView.as_view(), name="book_list"),
]
