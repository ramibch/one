from django.contrib.admin.sites import AdminSite

from one.articles.admin import (
    ArticleAdmin,
    ArticleFileAdmin,
    ArticlesSubmoduleAdmin,
)
from one.articles.models import Article, ArticleFile, ArticleParentFolder
from one.test import TestCase


class MockRequest:
    pass


class TestAdmin(TestCase):
    def setUp(self):
        # Create a mock admin site
        self.admin_site = AdminSite()

        # Mock request factory
        self.request = MockRequest()

    def test_article_parent_folder_perms(self):
        folder_admin = ArticlesSubmoduleAdmin(ArticleParentFolder, self.admin_site)
        self.assertFalse(folder_admin.has_delete_permission(self.request))
        self.assertFalse(folder_admin.has_add_permission(self.request))

    def test_article_perms(self):
        article_admin = ArticleAdmin(Article, self.admin_site)
        self.assertFalse(article_admin.has_delete_permission(self.request))
        self.assertFalse(article_admin.has_add_permission(self.request))

    def test_article_file_perms(self):
        article_file_admin = ArticleFileAdmin(ArticleFile, self.admin_site)
        self.assertFalse(article_file_admin.has_add_permission(self.request))
