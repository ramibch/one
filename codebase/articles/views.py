

from django.shortcuts import render
from django.utils import timezone
from django.views.generic.detail import DetailView

from .models import Article


class ArticleDetailView(DetailView):
    # template_name = "article.html"
    model = Article
