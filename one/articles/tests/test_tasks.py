from unittest.mock import patch

from one.sites.models import Site
from one.test import TestCase

from ..models import ArticleParentFolder
from ..tasks import sync_articles


class TestSyncArticles(TestCase):
    @patch("one.base.utils.abstracts.BaseSubmoduleFolder.fetch_submodules")
    def test_sync_articles_with_dev_sites(self, mock_method):
        ArticleParentFolder.sync_folders()
        test_folder = ArticleParentFolder.objects.get(name="test-folder")
        sites = Site.objects.all()
        for index, site in enumerate(sites):
            if index % 2:
                site.article_folders.add(test_folder)
        task_result = sync_articles(sites)

        self.assertIsNone(task_result())
        self.assertTrue(mock_method.called)
