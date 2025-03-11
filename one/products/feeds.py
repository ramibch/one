from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _

from one import settings

from .models import EtsyListing, Product


class ProductPinFeed(Feed):
    DAYS = 90
    title = _("List of products")
    link = "/"
    description = _("Last products published in my sites")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang: str) -> None:
        assert lang in settings.LANGUAGE_CODES
        activate(lang)
        super().__init__()

    def items(self):
        past = timezone.now() - timezone.timedelta(days=self.DAYS)
        return Product.objects.filter(
            created_on__gte=past,
            productimage__isnull=False,
        )

    def item_title(self, item: Product):
        return item.title

    def item_description(self, item: Product):
        return item.description

    def item_lastupdated(self, item: Product):
        return item.updated_on

    def item_enclosure_url(self, item: Product):
        return item.productimage_set.first().file.url

    def item_enclosure_length(self, item: Product):
        return item.productimage_set.first().file.size


class EtsyListingPinFeed(Feed):
    DAYS = 90
    title = _("List of Etsy listings")
    link = "/"
    description = _("Last products published in my sites as Etsy listings")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang: str) -> None:
        assert lang in settings.LANGUAGE_CODES
        activate(lang)
        super().__init__()

    def items(self):
        past = timezone.now() - timezone.timedelta(days=self.DAYS)
        return EtsyListing.objects.filter(
            created_on__gte=past,
            product__productimage__isnull=False,
        )

    def item_title(self, item: EtsyListing):
        return item.get_title()

    def item_description(self, item: EtsyListing):
        return item.get_description()

    def item_lastupdated(self, item: EtsyListing):
        return item.updated_on

    def item_enclosure_url(self, item: EtsyListing):
        return item.product.productimage_set.first().file.url

    def item_enclosure_length(self, item: EtsyListing):
        return item.product.productimage_set.first().file.size
