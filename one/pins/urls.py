from django.conf import settings
from django.urls import path

from . import feeds

# https://de.pinterest.com/settings/bulk-create-pins/


i18n_feeds = {
    # key/{lang}
    "pins/yearly-calendars": feeds.YearlyHolidayCalenderPinFeed,
    "products/pins/products": feeds.ProductPinFeed,
    "products/pins/etsy": feeds.EtsyListingPinFeed,
}


urlpatterns = [
    path(f"{url_prefix}/{lang}", feed_class(lang))
    for url_prefix, feed_class in i18n_feeds.items()
    for lang in settings.LANGUAGE_CODES
] + [
    path("dgt/pins/questions", feeds.DgtQuestionPinFeed()),  # add to i18n_feeds?
    path("dgt/pins/english-quiz-questions", feeds.EnglishQuizLectionFeed()),
]
