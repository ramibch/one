from django.conf import settings
from django.contrib.sitemaps import Sitemap

from one.articles.models import Article
from one.tools.tools import get_active_tools


class ArticleSitemap(Sitemap):
    i18n = True
    languages = settings.LANGUAGE_CODES
    changefreq = "daily"
    priority = 0.7

    def items(self):
        # TODO: fix!!!
        folders = self.request.site.article_folders.all()
        return Article.objects.filter(
            languages__in=[self.lang],
            parent_folder__in=folders,
            slug__isnull=False,
        )

    def lastmod(self, obj: Article):
        return obj.updated_on


class ToolSitemap(Sitemap):
    priority = 0.7
    changefreq = "never"

    def items(self):
        return get_active_tools()

    def location(self, item):
        return item.url


def get_sitemaps(*args, **kwargs):
    return {
        "articles": ArticleSitemap(),
        "tools": ToolSitemap(),
    }
