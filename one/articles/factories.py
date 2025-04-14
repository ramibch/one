from factory import Faker, SubFactory
from factory.django import DjangoModelFactory, FileField

from one.users.factories import UserFactory

from .models import Article, ArticleFile, Comment, MainTopic


class ArticleParentFolderFactory(DjangoModelFactory):
    name = Faker("word")

    class Meta:
        model = MainTopic
        django_get_or_create = ("name",)


class ArticleFactory(DjangoModelFactory):
    main_topic = SubFactory(ArticleParentFolderFactory)
    title = Faker("sentence")
    slug = Faker("slug")
    folder_name = Faker("word")
    subfolder_name = Faker("slug")
    body = Faker("text")

    class Meta:
        model = Article
        django_get_or_create = ("slug",)


class ArticleFileFactory(DjangoModelFactory):
    article = SubFactory(ArticleFactory)
    file = FileField(filename="dummyfile.dat")
    name = Faker("word")

    class Meta:
        model = ArticleFile


class CommentFactory(DjangoModelFactory):
    article = SubFactory(ArticleFactory)
    author = SubFactory(UserFactory)
    content = Faker("sentence")

    class Meta:
        model = Comment
