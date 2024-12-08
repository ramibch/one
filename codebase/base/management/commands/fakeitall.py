from django.conf import settings
from django.core.management.base import BaseCommand

from codebase.sites.models import Site

from ....articles.factories import ArticleFactory, ArticlesFolderFactory
from ...utils.decorators import check_sites_settings_for_cmd


def get_sites(options):
    for env in options["environments"]:
        for _, domain in settings.SITES[env]:
            yield Site.objects.filter(domain=domain)


class Command(BaseCommand):
    help = "Fake data"

    def add_arguments(self, parser):
        parser.add_argument("environments", nargs="+", type=str)

    @check_sites_settings_for_cmd
    def handle(self, *args, **options):
        for sites in get_sites(options):
            # Article folders and articles itself
            article_folders = ArticlesFolderFactory.create_batch(5)
            for article_folder in article_folders:
                ArticleFactory.create_batch(10, submodule=article_folder)
                article_folder.sites.set(sites)

            # Page folders and pages itself

            # FAQs (multiple per site)

            # HomePage (one active per site?)

            # UserHomePage
