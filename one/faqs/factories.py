import factory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import FAQ, FAQCategory

faker = Faker()


class FAQCategoryFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = FAQCategory


class FAQFactory(DjangoModelFactory):
    question = factory.LazyAttribute(lambda _: f"{faker.sentence().replace('.', '?')}")
    answer = factory.Faker("text")

    class Meta:
        model = FAQ

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.sites.add(*extracted)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.categories.add(*extracted)
