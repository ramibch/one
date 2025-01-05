from one.test import TestCase

from ..factories import ArticleFactory
from ..models import Article
from ..sitemaps import ArticleSitemap


class TestArticleSitemap(TestCase):
    def setUp(self):
        self.count = 5
        ArticleFactory.create_batch(self.count)
        self.sitemap = ArticleSitemap()

    def test_items(self):
        self.assertEqual(self.sitemap.items().count(), self.count)

    def test_lastmod(self):
        obj = Article.objects.last()
        self.assertIsNotNone(self.sitemap.lastmod(obj))
        self.assertEqual(obj.updated_on, self.sitemap.lastmod(obj))
