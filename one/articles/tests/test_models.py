from one.test import TestCase

from ..factories import (
    ArticleFactory,
    ArticleFileFactory,
    ArticleParentFolderFactory,
    CommentFactory,
)


class TestArticleParentFolder(TestCase):
    def test_str_method(self):
        obj = ArticleParentFolderFactory()
        self.assertIsInstance(str(obj), str)


class TestArticle(TestCase):
    def setUp(self):
        self.obj = ArticleFactory()

    def test_str_method(self):
        self.assertIsInstance(str(self.obj), str)

    def test_get_absolute_url(self):
        self.assertIsInstance(str(self.obj.get_absolute_url()), str)
        self.assertTrue(self.obj.get_absolute_url().isprintable())


class TestArticleFileFactory(TestCase):
    def setUp(self):
        self.obj = ArticleFileFactory()

    def test_str_method(self):
        self.assertIsInstance(str(self.obj), str)


class TestCommentFactory(TestCase):
    def test_str_method(self):
        obj = CommentFactory()
        self.assertIsInstance(str(obj), str)
