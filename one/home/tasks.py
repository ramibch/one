from huey import crontab
from huey.contrib import djhuey as huey

from ..articles.models import Article
from ..faqs.models import FAQ
from .models import ArticlesSection, FAQsSection


@huey.db_periodic_task(crontab(minute="30"))
def auto_add_artciles_to_sections():
    """
    Task to add articles in Home Article Sections
    """
    for section in ArticlesSection.objects.filter(auto_add_articles=True):
        articles = Article.objects.filter(
            parent_folder__in=section.home.site.article_folders.all(),
            featured=True,
        )
        section.articles.add(*articles)


@huey.db_periodic_task(crontab(minute="31"))
def auto_add_faqs_to_sections():
    """
    Task to add articles in Home Article Sections
    """
    for section in FAQsSection.objects.filter(auto_add_faqs=True):
        faqs = FAQ.objects.filter(
            sites=section.home.site,
            featured=True,
            category__in=section.auto_add_categories,
        )
        section.faqs.add(*faqs)
