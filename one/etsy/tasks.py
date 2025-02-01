from huey.contrib import djhuey as huey

from one.products.models import Product

from .models import Listing


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
            if Listing.objects.filter(product=product, shop=shop).exists():
                continue
            listings.append(
                Listing(
                    product=product,
                    shop=shop,
                    price=shop.price_percentage / 100 * product.price,
                )
            )
    Listing.objects.bulk_create(listings)
