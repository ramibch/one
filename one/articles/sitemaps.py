from django.conf import settings
from django.contrib.sitemaps import Sitemap

from .models import Article


class ArticleSitemap(Sitemap):
    i18n = True
    languages = settings.LANGUAGE_CODES
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Article.objects.filter()

    def lastmod(self, obj: Article):
        return obj.updated_on
