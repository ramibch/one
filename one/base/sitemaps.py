from ..articles.sitemaps import ArticleSitemap
from ..pages.sitemaps import PageSitemap
from ..tools.sitemaps import ToolSitemap


def get_sitemaps():
    return {
        "articles": ArticleSitemap(),
        "pages": PageSitemap(),
        "tools": ToolSitemap(),
    }
