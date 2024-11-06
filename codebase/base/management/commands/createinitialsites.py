from django.core.management.base import BaseCommand, CommandError


from django.contrib.sites.models import Site

from ...models import Website

from django.conf import settings

class Command(BaseCommand):
    help = "By default creates initial sites that are defined in the setting INITIAL_SITES"

    def add_arguments(self, parser):
        parser.add_argument("--delete-example-site", action="store_true",help="Remove previously the site example.com")
        parser.add_argument("--delete-all-sites", action="store_true",help="Remove previously all the sites")
        parser.add_argument("--delete-all-websites", action="store_true",help="Remove previously all the websites")


    def handle(self, *args, **options):

        if options["delete_example_site"]:
            Site.objects.filter(domain="example.com").delete()

        if options["delete_all_sites"]:
            Site.objects.all().delete()

        if options["delete_all_websites"]:
            Website.objects.all().delete()


        existing_sites = Site.objects.all()
        if existing_sites.count() > 0:
            site_list_as_str = "\n".join([site.domain for site in existing_sites])
            raise CommandError(f"Sites are already created.\n{site_list_as_str}")

        initial_sites = getattr(settings, "INITIAL_SITES", None)

        if initial_sites is None:
            raise CommandError(f"The setting INITIAL_SITES is not defined.")

        created_websites = []

        for site_name, site_domain in initial_sites:
            # Sites objects are automatically created when their Website are created
            created_websites.append(Website.objects.create(name=site_name, domain=site_domain))

        created_websites_as_str = "\n".join([site.domain for site in created_websites])
        self.stdout.write(self.style.SUCCESS(f"Websites and Sites successfully created:\n{created_websites_as_str}"))

