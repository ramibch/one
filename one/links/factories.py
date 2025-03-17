import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from .models import DJ_PATHS

faker = Faker()


class LinkFactory(DjangoModelFactory):
    language = factory.Iterator(settings.LANGUAGE_CODES)
    languages = ["en", "de", "es"]
    custom_title = factory.LazyAttribute(lambda _: faker.sentence())
    external_url = factory.LazyAttribute(lambda _: faker.url())
    django_url_path = factory.Iterator([p[0] for p in DJ_PATHS])
    page = None  # TODO: factory.SubFactory(PageFactory) with "00_test" folder
    article = None  # TODO: factory.SubFactory(ArticleFactory)  with "00_test" folder
    plan = None  # TODO: factory.SubFactory(PlanFactory)
    topic = None  # TODO: factory.SubFactory(TopicFactory) )
