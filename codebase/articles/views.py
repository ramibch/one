from django.views.generic.list import ListView

from .models import Article

from ..base.generic_views import MultilinguageDetailView


class ArticleDetailView(MultilinguageDetailView):
    model = Article


class ArticleListView(ListView):
    model = Article

