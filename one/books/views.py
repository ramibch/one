from django.views.generic.list import ListView

from one.base.utils.generic_views import MultilinguageDetailView

from .models import Book


class BookDetailView(MultilinguageDetailView):
    model = Book


class BookListView(ListView):
    model = Book
