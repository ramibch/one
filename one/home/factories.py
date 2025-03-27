import factory
from factory.django import DjangoModelFactory
from faker import Faker

from one.links.factories import LinkFactory
from one.sites.factories import SiteFactory

from .models import (
    ArticlesSection,
    BenefitsSection,
    FAQsSection,
    HeroSection,
    Home,
    ProblemSection,
    SolutionSection,
    StepAction,
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


class ArticlesSectionFactory(HomeChildModelFactory):
    title = factory.LazyAttribute(lambda _: faker.sentence())
    number_of_articles = factory.LazyAttribute(lambda _: faker.random_number())
    card_animation = None  # TODO:

    class Meta:
        model = ArticlesSection


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


class SolutionSectionFactory(HomeChildModelFactory):
    class Meta:
        model = SolutionSection


class BenefitsSectionFactory(HomeChildModelFactory):
    class Meta:
        model = BenefitsSection


class StepActionFactory(HomeChildModelFactory):
    class Meta:
        model = StepAction


class FAQsSectionFactory(HomeChildModelFactory):
    class Meta:
        model = FAQsSection
