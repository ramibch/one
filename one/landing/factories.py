import factory
from factory.django import DjangoModelFactory
from faker import Faker

from one.links.factories import LinkFactory
from one.sites.factories import SiteFactory

from .models import (
    ArticlesSection,
    BenefitItem,
    FAQsSection,
    FinalCTASection,
    HeroSection,
    LandingPage,
    ProblemSection,
    SolutionSection,
    StepActionSection,
)

faker = Faker()


class LandingPageFactory(DjangoModelFactory):
    title = factory.LazyAttribute(lambda _: faker.sentence())
    site = factory.SubFactory(SiteFactory)

    class Meta:
        model = LandingPage


class LandingPageChildModelFactory(DjangoModelFactory):
    home = factory.SubFactory(LandingPageFactory)

    class Meta:
        abstract = True


class HeroSectionFactory(LandingPageChildModelFactory):
    headline = factory.LazyAttribute(lambda _: faker.sentence())
    subheadline = factory.LazyAttribute(lambda _: faker.sentence())
    image = factory.django.ImageField()
    cta_link = factory.SubFactory(LinkFactory)
    cta_title = factory.LazyAttribute(lambda _: faker.sentence())
    cta_new_tab = factory.LazyAttribute(lambda _: faker.boolean())
    cta_animation = None  # TODO:

    class Meta:
        model = HeroSection


class ProblemSectionFactory(LandingPageChildModelFactory):
    class Meta:
        model = ProblemSection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(
        lambda _: "\n".join(f"- {faker.sentence()}" for _ in range(4)) + "\n"
    )


class SolutionSectionFactory(LandingPageChildModelFactory):
    class Meta:
        model = SolutionSection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: (faker.text(max_nb_chars=400)))


class BenefitItemFactory(LandingPageChildModelFactory):
    class Meta:
        model = BenefitItem

    emoji = factory.Iterator(["🎁", "🦊", "🚀", "✅", "📚"])
    name = factory.LazyAttribute(lambda _: faker.sentence(nb_words=2))
    description = factory.LazyAttribute(lambda _: faker.paragraph())


class StepActionSectionFactory(LandingPageChildModelFactory):
    class Meta:
        model = StepActionSection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: (faker.text(max_nb_chars=400)))


class ArticlesSectionFactory(LandingPageChildModelFactory):
    title = factory.LazyAttribute(lambda _: faker.sentence())
    number_of_articles = factory.LazyAttribute(lambda _: faker.random_number())
    card_animation = None  # TODO:

    class Meta:
        model = ArticlesSection


class FAQsSectionFactory(LandingPageChildModelFactory):
    class Meta:
        model = FAQsSection

    title = factory.LazyAttribute(lambda _: faker.sentence(nb_words=4))

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.categories.add(*extracted)


class FinalCTASectionFactory(LandingPageChildModelFactory):
    class Meta:
        model = FinalCTASection

    title = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: (faker.text(max_nb_chars=200)))
    cta_link = factory.SubFactory(LinkFactory)
    cta_title = factory.LazyAttribute(lambda _: faker.sentence())
    cta_new_tab = factory.LazyAttribute(lambda _: faker.boolean())
