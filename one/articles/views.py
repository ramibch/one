from django.db.models import QuerySet
from django.utils.translation import get_language
from django.views.generic.list import ListView

from one.articles.models import Article


class ArticleListView(ListView):
    model = Article

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(
            languages__contains=[get_language()],
            main_topic__name__in=self.request.site.topics,
        )
