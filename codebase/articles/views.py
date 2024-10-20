from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
