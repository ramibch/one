import random
from functools import cache
from mimetypes import guess_type

import auto_prefetch
from auths.models import Pinterest
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField
from pinterest.organic.pins import Pin
from socialmedia.models import FacebookGroup, LinkedinGroup, TelegramGroup
from socialmedia.tasks import create_linkedin_post
from utils.telegram import report_to_admin
from utils.webdrivers import Facebook

from .listings import Listing


def upload_article_file(obj, filename):
    return f"articles/{obj.article.slug}/{filename}"


class AbstractPage(auto_prefetch.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=180)
    slug = models.SlugField(max_length=128, unique=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    def get_absolute_url(self):
        return reverse("page-detail", kwargs={"slug": self.slug})

    @cached_property
    def page_url(self):
        return self.get_absolute_url()

    @cached_property
    def anchor_tag(self):
        return mark_safe(f"<a target='_blank' href='{self.page_url}'>{self.title}</a>")

    @cached_property
    def full_page_url(self):
        return settings.WEBSITE_URL + self.page_url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(AbstractPage, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class ListingTag(auto_prefetch.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class ListingProduct(auto_prefetch.Model):
    template_name = "product.html"
    dirname = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to="listings", null=True)
    topics = models.ManyToManyField(Topic)
    tags = models.ManyToManyField(ListingTag)
    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )
    public = models.BooleanField(default=False)
    promoted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dirname

    def get_listing(self):
        return Listing.objects.get(dirname=self.dirname)

    @cached_property
    def description(self):
        return self.get_listing().get_description()

    @cached_property
    def gumroad_url(self):
        if (
            self.get_listing().gumroad_url != ""
            and self.get_listing().gumroad_url is not None
        ):
            return self.get_listing().gumroad_url

    @cached_property
    def etsy_url(self):
        if (
            self.get_listing().etsy_url != ""
            and self.get_listing().etsy_url is not None
        ):
            return self.get_listing().etsy_url

    @cached_property
    def page_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return reverse("page-detail", kwargs={"slug": self.dirname})

    @cached_property
    def full_page_url(self):
        return settings.WEBSITE_URL + self.page_url

    @cached_property
    def price(self):
        return self.get_listing().price

    @cached_property
    def price_in_cents(self):
        return int(self.price * 100)

    @cached_property
    def title(self):
        return self.get_listing().title

    @cached_property
    def keywords(self):
        return self.get_listing().keywords

    @cached_property
    def listing_type(self):
        return self.get_listing().listing_type

    @cached_property
    def checkout_url(self):
        return reverse("product-checkout", kwargs={"id": self.id})

    def get_pinterest_board_id(self):
        boards = {"etsy": "922745479841573954"}
        return boards[self.site]

    def promote_in_pinterest(self):
        # May 2024: not used since I do not have access to the API
        Pin.create(
            board_id=self.get_pinterest_board_id(),
            media_source={
                "source_type": "image_url",
                "content_type": guess_type(self.image.url)[0],
                "data": "string",
                "url": self.image.url,
            },
            link=self.full_page_url,
            title=self.title,
            description=None,
            dominant_color=None,
            alt_text=self.title,
            board_section_id=None,
            parent_pin_id=None,
            client=Pinterest.load().get_api_client(),
        )

    def promote_in_facebook(self) -> str:
        groups = FacebookGroup.objects.filter(
            listing_tags__in=self.tags.all(), language=self.language, active=True
        ).distinct()

        if groups.count() == 0:
            return "⚠️ No Facebooks groups found to promote\n"

        fb = Facebook()
        out = "Facebook:\n"
        for index, fb_group in enumerate(groups, start=1):
            try:
                fb.post_in_group(
                    self.get_full_promotion_text(),
                    group_id=fb_group.group_id,
                    filepath_str=self.get_image_local_path_str(),
                    close_driver=index == groups.count(),
                )
                out += f"✔ Posted in facebook group {fb_group.url}\n"
            except Exception as e:
                out += f"❌ Exception in  facebook group: {e}\n"
                if index == groups.count():
                    fb.driver.close()

        return out

    def promote_in_linkedin(self):
        groups = LinkedinGroup.objects.filter(
            listing_tags__in=self.tags.all(),
            language=self.language,
            active=True,
        ).distinct()

        if groups.count() == 0:
            return "⚠️ No Linkedin groups found to promote\n"

        post = create_linkedin_post(self.get_full_promotion_text(), self.image)
        out = "Linkedin:\n"
        for li_group in groups:
            try:
                post.share(visibility=li_group.visibility, container=li_group.container)
                out += f"✔ Posted in Linkedin group {li_group.url}\n"
            except Exception as e:
                out += f"❌ Exception in  Linkedin group: {e}\n"
        return out

    def promote(self):
        reporting = f"Promoting: {self.title}\n"

        # Promote in Facebook
        try:
            reporting += self.promote_in_facebook()
        except Exception as e:
            reporting += f"❌ Error promoting in Facebook: {e}\n"

        # Promote in Linkedin
        try:
            reporting += self.promote_in_linkedin()
        except Exception as e:
            reporting += f"❌ Error promoting in Linkedin: {e}\n"

        # Report to admin
        report_to_admin(reporting)
        # Save state in db
        self.promoted = True
        self.save()

    def get_full_promotion_text(self):
        intro = {
            "es": "Hola a todos! Quizá os interese lo que he creado recientemente...",
            "en": "Hi all! You might be interested in what I have recently created...",
            "de": "Hallo Leute! Vielleicht interessiert es euch, was ich kürzlich erstellt habe...",
        }
        links = [self.full_page_url, self.etsy_url, self.gumroad_url]
        content = intro[self.language] + "\n\n"
        content += self.title + "\n\n"
        content += random.choice([link for link in links if link is not None])
        return content

    def get_image_local_path_str(self):
        try:
            return str(list(self.get_listing().images_path.iterdir())[0])
        except Exception:
            pass


class Article(AbstractPage):
    """Article page"""

    template_name = "article.html"

    home_listing = models.BooleanField(default=False)

    published_in_medium = models.BooleanField(default=False)

    topic = models.ForeignKey(Topic, null=True, on_delete=models.CASCADE)

    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )

    body = MarkdownxField(null=True)

    @cached_property
    def related_listing_products(self):
        return ListingProduct.objects.filter(
            topics__id=self.topic.id, language=self.language, public=True
        ).distinct()[:10]

    @cached_property
    def related_telegram_groups(self):
        return TelegramGroup.objects.filter(
            active=True, topics__id=self.topic.id, language=self.language
        ).distinct()

    def create_social_post(self):
        from socialmedia.models import SocialPost

        if self.language == "es":
            text = "Échale un vistazo al articulo que acabo de escribir: \n\n"
        elif self.language == "de":
            text = "Schau den Artikel an, den ich gerade geschrieben habe: \n\n"
        elif "de" in self.language:
            text = "Have a look at the article I have just written: \n\n"
        text += self.title + "\n\n"
        text += self.full_page_url
        SocialPost.objects.create(text=text)


class ArticleFile(auto_prefetch.Model):
    article = auto_prefetch.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True)
    file = models.FileField(upload_to=upload_article_file)


class Home(AbstractPage):
    """Home page"""

    template_name = "home.html"

    language = models.CharField(
        max_length=8, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )

    @cached_property
    def related_articles(self):
        return Article.objects.filter(
            public=True, home_listing=True, language=self.language
        )

    @cached_property
    def related_products(self):
        return ListingProduct.objects.filter(language=self.language, public=True)[:6]

    @cached_property
    def related_mobile_apps(self):
        from mobile.models import App

        return App.objects.filter(language=self.language)

    @cached_property
    def related_pages(self):
        return Page.objects.filter(public=True, language=self.language)

    @cached_property
    def related_telegram_groups(self):
        return TelegramGroup.objects.filter(
            active=True, language=self.language
        ).distinct()


class MenuListItem(auto_prefetch.Model):
    title = models.CharField(max_length=128)
    show_in_navbar = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    class Meta(auto_prefetch.Model.Meta):
        ordering = ("order",)


class PageLink(auto_prefetch.Model):
    menu = auto_prefetch.ForeignKey(MenuListItem, on_delete=models.CASCADE, null=True)
    page = auto_prefetch.ForeignKey(
        Page, on_delete=models.CASCADE, null=True, blank=True
    )
    topic = auto_prefetch.ForeignKey(
        Topic, on_delete=models.CASCADE, null=True, blank=True
    )
    external_title = models.CharField(max_length=128, null=True, blank=True)
    external_url = models.URLField(max_length=128, null=True, blank=True)
    target_blank = models.BooleanField(default=False)

    @cached_property
    def url(self):
        if self.page is not None:
            return self.page.page_url
        elif self.topic is not None:
            return self.topic.page_url
        elif self.external_url is not None:
            return self.external_url
        return ""

    @cached_property
    def title(self):
        if self.page is not None:
            return self.page.title
        if self.topic is not None:
            return self.topic.name
        else:
            return self.external_title

    def __str__(self):
        return self.title


class SearchTerm(models.Model):
    q = models.TextField(max_length=128)

    def __str__(self) -> str:
        return self.q


@cache
def get_page_object(slug):
    """Return a page like object if it exists. If not, return none"""
    for Model in (Article, Page, Topic):
        try:
            return Model.objects.get(slug=slug)
        except Model.DoesNotExist:
            pass

    try:
        return ListingProduct.objects.get(dirname=slug)
    except ListingProduct.DoesNotExist:
        pass


class Feedback(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField(verbose_name=_("Message"), max_length=1024)

    def __str__(self):
        return self.message[:100]
