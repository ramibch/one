import factory

from .models import Article, ArticleParentFolder


class ArticleParentFolderFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = ArticleParentFolder
        django_get_or_create = ("name",)


class ArticleFactory(factory.django.DjangoModelFactory):
    parent_folder = factory.SubFactory(ArticleParentFolderFactory)
    title = factory.Faker("sentence")
    slug = factory.Faker("slug")
    folder_name = factory.Faker("word")
    subfolder_name = factory.Faker("slug")
    body = factory.Faker("text")

    class Meta:
        model = Article
        django_get_or_create = ("slug",)
