import factory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import FAQ, FAQCategory

faker = Faker()


class FAQFactory(DjangoModelFactory):
    category = factory.Iterator(FAQCategory.values)
    question = factory.LazyAttribute(lambda _: f"{faker.sentence().replace(".", "?")}")
    answer = factory.Faker("text")
    featured = factory.Faker("boolean", chance_of_getting_true=80)

    class Meta:
        model = FAQ

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.sites.add(*extracted)
