from random import randint, sample

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from one.faqs.models import FAQCategory
from one.links.factories import LinkFactory
from one.sites.factories import SiteFactory

from .models import (
    ArticlesSection,
    BenefitItem,
    FAQsSection,
    FinalCTASection,
    HeroSection,
    Home,
    ProblemSection,
    SolutionSection,
    StepActionSection,
)

faker = Faker()


class HomeFactory(DjangoModelFactory):
    title = factory.LazyAttribute(lambda _: faker.sentence())
    site = factory.SubFactory(SiteFactory)

    class Meta:
        model = Home


class HomeChildModelFactory(DjangoModelFactory):
    home = factory.SubFactory(HomeFactory)

    class Meta:
        abstract = True


class HeroSectionFactory(HomeChildModelFactory):
    headline = factory.LazyAttribute(lambda _: faker.sentence())
    subheadline = factory.LazyAttribute(lambda _: faker.sentence())
    image = factory.django.ImageField()
    cta_link = factory.SubFactory(LinkFactory)
    cta_title = factory.LazyAttribute(lambda _: faker.sentence())
    cta_new_tab = factory.LazyAttribute(lambda _: faker.boolean())
    cta_animation = None  # TODO:

    class Meta:
        model = HeroSection


class ProblemSectionFactory(HomeChildModelFactory):
    class Meta:
        model = ProblemSection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(
        lambda _: "\n".join(f"- {faker.sentence()}" for _ in range(4)) + "\n"
    )


class SolutionSectionFactory(HomeChildModelFactory):
    class Meta:
        model = SolutionSection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: (faker.text(max_nb_chars=400)))


class BenefitItemFactory(HomeChildModelFactory):
    class Meta:
        model = BenefitItem

    emoji = factory.Iterator(["🎁", "🦊", "🚀", "✅", "📚"])
    name = factory.LazyAttribute(lambda _: faker.sentence(nb_words=2))
    description = factory.LazyAttribute(lambda _: faker.paragraph())


class StepActionSectionFactory(HomeChildModelFactory):
    class Meta:
        model = StepActionSection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: (faker.text(max_nb_chars=400)))


class ArticlesSectionFactory(HomeChildModelFactory):
    title = factory.LazyAttribute(lambda _: faker.sentence())
    number_of_articles = factory.LazyAttribute(lambda _: faker.random_number())
    card_animation = None  # TODO:

    class Meta:
        model = ArticlesSection


class FAQsSectionFactory(HomeChildModelFactory):
    class Meta:
        model = FAQsSection

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=4))
    categories = factory.List(
        sample(FAQCategory.values, k=randint(1, len(FAQCategory.values)))
    )


class FinalCTASectionFactory(HomeChildModelFactory):
    class Meta:
        model = FinalCTASection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: (faker.text(max_nb_chars=200)))
    cta_link = factory.SubFactory(LinkFactory)
    cta_title = factory.LazyAttribute(lambda _: faker.sentence())
    cta_new_tab = factory.LazyAttribute(lambda _: faker.boolean())
