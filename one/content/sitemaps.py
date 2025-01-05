from django.contrib.sitemaps import Sitemap

from .models import Article, ListingProduct, Topic


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8

    def items(self):
        return Article.objects.filter(public=True)

    def lastmod(self, obj):
        return obj.updated_on


class TopicSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7

    def items(self):
        return Topic.objects.filter(public=True)


class ProductSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return ListingProduct.objects.all()

    def lastmod(self, obj):
        return obj.updated_on


def get_sitemaps():
    sitemaps = {
        "topics": TopicSitemap(),
        "articles": ArticleSitemap(),
        "products": ProductSitemap(),
    }
    return sitemaps
