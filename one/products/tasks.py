from django.core.files import File
from huey import crontab
from huey.contrib import djhuey as huey

from ..base.utils.telegram import Bot
from .models import EtsyListing, Product, ProductFile, ProductImage


@huey.db_periodic_task(crontab(hour="4", minute="10"))
def sync_products():
    """
    Sync products
    """

    Product.sync_folders()

    submodule = Product.submodule
    submodule_path = Product.submodule_path

    log = f"🔄 Syncing {submodule}\n\n"

    # Scanning
    for product in Product.objects.all():
        folder = submodule_path / product.name

        if not folder.is_dir():
            product.present_in_filesystem = False
            product.save()
            continue

        for subfolder in folder.iterdir():
            if not subfolder.is_dir():
                continue

            log += f"🎁 {product}/{subfolder.name}\n"

            if subfolder.name == "files":
                FileModel = ProductFile
            elif subfolder.name == "images":
                FileModel = ProductImage
            else:
                continue

            # Files
            for file_path in (p for p in subfolder.iterdir()):
                if file_path.is_dir():
                    continue

                db_file = FileModel.objects.get_or_create(
                    product=product,
                    name=file_path.name,
                )[0]
                db_file.file = File(file_path.open(mode="rb"), name=file_path.name)
                db_file.save()

    Bot.to_admin(log)


@huey.db_task()
def task_upload_listings(listings):
    """
    Uploading listings to Etsy
    """
    for listing in listings:
        listing.upload_to_etsy()


@huey.db_task()
def task_generate_listings_from_products(shops):
    """
    Create listings from Product objects
    """
    listings = []
    for shop in shops:
        products = Product.objects.filter(topics__in=shop.topics.all())
        for product in products:
            if EtsyListing.objects.filter(product=product, shop=shop).exists():
                continue
            listings.append(
                EtsyListing(
                    product=product,
                    shop=shop,
                    price=shop.price_percentage / 100 * product.price,
                )
            )
    EtsyListing.objects.bulk_create(listings)
