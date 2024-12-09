"""maybe create 'process_mfiles.py' > to generate articles + listing items"""

from django.core.management.base import BaseCommand
from django.db import transaction

from utils.webdrivers import Gumroad

from ...listings import LISTINGS_PATH, Listing


class Command(BaseCommand):
    help = "Upload listing to gumroad site"

    @transaction.atomic
    def handle(self, *args, **options):
        dirnames = (d.name for d in LISTINGS_PATH.iterdir())
        gumroad = Gumroad()
        for dirname in dirnames:
            try:
                listing = Listing.objects.get(dirname=dirname)
                if not listing.gumroad_url == "":
                    continue
            except Exception as e:
                print(f"Error Listing: {dirname}: {e}")
                continue
            try:
                listing.upload_to_gumroad(gumroad)
            except Exception as e:
                print(f"Error Gumroad: {dirname}: {e}")
                continue
            listing.set_gumroad_url(dirname)
