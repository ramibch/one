from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _

from .models import Product


class EtsyProductPinFeed(Feed):
    """Base Feed Product that are in Etsy"""

    DAYS = 90
    title = _("Etsy listings")
    link = "/"
    description = _("Etsy listing published in my shop.")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang) -> None:
        self.lang = lang
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
        return item.productimage_set.first().url

    def item_enclosure_length(self, item: Product):
        return item.productimage_set.first().size
