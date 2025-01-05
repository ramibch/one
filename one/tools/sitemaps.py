from django.contrib.sitemaps import Sitemap

from .tools import get_active_tools


class ToolSitemap(Sitemap):
    priority = 0.7
    changefreq = "never"

    def items(self):
        return get_active_tools()

    def location(self, item):
        return item.url
