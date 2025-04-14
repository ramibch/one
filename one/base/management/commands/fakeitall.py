from django.core.management.base import BaseCommand

from one.sites.models import Site

from ....articles.factories import ArticleFactory, ArticleParentFolderFactory


class Command(BaseCommand):
    help = "Fake data"

    def add_arguments(self, parser):
        parser.add_argument("site_names", nargs="+", type=str)

    def get_sites(self, options):
        for site_name in options["site_names"]:
            yield Site.objects.filter(name=site_name)

    def handle(self, *args, **options):
        for site in self.get_sites(options):
            # Article folders and articles itself
            article_folders = ArticleParentFolderFactory.create_batch(5)
            for article_folder in article_folders:
                ArticleFactory.create_batch(10, main_topic=article_folder)
            article_folder.sites.set(site)

            # Page folders and pages itself

            # FAQs (multiple per site)

            # HomePage (one active per site?)
