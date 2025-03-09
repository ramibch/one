from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import DgtQuestion


class DgtQuestionPinFeed(Feed):
    """DGT Question Feed for Pinterest"""

    DAYS = 90
    title = "DGT tests anteriores"
    link = "/"
    description = "DGT tests anteriores"
    item_enclosure_mime_type = "image/png"

    def items(self):
        past = timezone.now() - timezone.timedelta(days=self.DAYS)
        return DgtQuestion.objects.filter(
            test__scrapped_on__gte=past,
            image__isnull=False,
        )

    def item_title(self, item: DgtQuestion):
        return item.title

    def item_description(self, item: DgtQuestion):
        return f"{item.title}\n\n{item.option_a}\n{item.option_b}\n{item.option_c}"

    def item_lastupdated(self, item: DgtQuestion):
        return item.test.scrapped_on

    def item_enclosure_url(self, item: DgtQuestion):
        return item.image.url

    def item_enclosure_length(self, item: DgtQuestion):
        return item.image.size
