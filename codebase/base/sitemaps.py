from ..articles.sitemaps import ArticleSitemap
from ..pages.sitemaps import PageSitemap


def get_sitemaps():
    return {
        "articles": ArticleSitemap(),
        "pages": PageSitemap(),
    }
