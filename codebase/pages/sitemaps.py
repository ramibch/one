from django.contrib.sitemaps import Sitemap

from .models import Page
from django.conf import settings


class PageSitemap(Sitemap):
    i18n = True
    languages = settings.LANGUAGE_CODES
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Page.objects.filter()

    def lastmod(self, obj: Page):
        return obj.updated_on
