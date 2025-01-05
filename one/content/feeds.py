from django.contrib.syndication.views import Feed

from .models import Article, ListingProduct


class RssListingFeeds(Feed):
    title = "Listings"
    link = "/"
    description = "Listings from ramiboutas.com"
    item_enclosure_mime_type = "image/png"

    def items(self):
        return ListingProduct.objects.filter(public=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_listing().get_description(general=False)

    def item_lastupdated(self, item):
        return item.updated_on

    def item_enclosure_url(self, item):
        return item.image.url

    def item_enclosure_length(self, item):
        return item.image.size


class RssArticleFeeds(Feed):
    title = "Articles"
    link = "/"
    description = "Articles from ramiboutas.com"

    def items(self):
        return Article.objects.filter(public=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_lastupdated(self, item):
        return item.updated_on
