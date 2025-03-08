from django.views.generic.list import ListView

from one.base.utils.generic_views import MultilinguageDetailView

from .models import Article


class ArticleDetailView(MultilinguageDetailView):
    model = Article


class ArticleListView(ListView):
    model = Article
