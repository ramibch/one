from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import gettext_lazy as _

from ..dgt.models import DgtQuestion
from ..products.models import EtsyListing, Product
from ..tex.models import EnglishQuizLection, YearlyHolidayCalender


class ProductPinFeed(Feed):
    title = _("List of products")
    link = "/"
    description = _("Last products published in my sites")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang: str) -> None:
        assert lang in settings.LANGUAGE_CODES
        activate(lang)
        super().__init__()

    def items(self):
        past = timezone.now() - timezone.timedelta(days=90)
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
    title = _("List of Etsy listings")
    link = "/"
    description = _("Last products published in my sites as Etsy listings")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang: str) -> None:
        assert lang in settings.LANGUAGE_CODES
        activate(lang)
        super().__init__()

    def items(self):
        past = timezone.now() - timezone.timedelta(days=90)
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


class DgtQuestionPinFeed(Feed):
    """DGT Question Feed for Pinterest"""

    title = "DGT tests anteriores"
    link = "/"
    description = "DGT tests anteriores"
    item_enclosure_mime_type = "image/png"

    def items(self):
        past = timezone.now() - timezone.timedelta(days=90)
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


class YearlyHolidayCalenderPinFeed(Feed):
    title = _("List of calendars")
    link = "/"
    description = _("Last calendars published in my sites")
    item_enclosure_mime_type = "image/png"

    def __init__(self, lang: str) -> None:
        assert lang in settings.LANGUAGE_CODES
        activate(lang)
        self.lang = lang
        super().__init__()

    def items(self):
        past = timezone.now() - timezone.timedelta(days=90)
        return YearlyHolidayCalender.objects.exclude(pdf="", image="").filter(
            created_on__gte=past, lang=self.lang
        )

    def item_title(self, item: YearlyHolidayCalender):
        return f"{str(_('Calendar'))} {item.year} | {item.title}"

    def item_description(self, item: YearlyHolidayCalender):
        return "\n".join(
            f"{d.strftime('%Y-%m-%d')} - {n}" for d, n in item.country_holidays
        )

    def item_lastupdated(self, item: YearlyHolidayCalender):
        return item.updated_on

    def item_enclosure_url(self, item: YearlyHolidayCalender):
        return item.image.url

    def item_enclosure_length(self, item: YearlyHolidayCalender):
        return item.image.size


class EnglishQuizLectionFeed(Feed):
    title = _("English quizzes")
    link = "/"
    description = _("Last English quizzes published in my site")
    item_enclosure_mime_type = "image/png"

    def items(self):
        past = timezone.now() - timezone.timedelta(days=90)
        return EnglishQuizLection.objects.exclude(pdf="", image="").filter(
            created_on__gte=past
        )

    def item_title(self, item: EnglishQuizLection):
        return f"{item.lection.quiz.name} | {item.lection.name}"

    def item_description(self, item: EnglishQuizLection):
        title = self.item_title(item)
        question_text = "\n".join(q.full_text for q in item.lection.question_set.all())
        return f"{title}\n\n{question_text}"

    def item_lastupdated(self, item: EnglishQuizLection):
        return item.created_on

    def item_enclosure_url(self, item: EnglishQuizLection):
        return item.image.url

    def item_enclosure_length(self, item: EnglishQuizLection):
        return item.image.size
