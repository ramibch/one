from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from ..articles.models import ArticlesFolder
from ..pages.models import PagesFolder
from ..utils.exceptions import SubmoduleFolderModelUnknow

User = get_user_model()


class ExtendedSite(Site):
    remarks = models.TextField(null=True, blank=True)

    emoji = models.CharField(max_length=8, null=True)
    emoji_in_brand = models.BooleanField(default=True)
    default_page_title = models.CharField(max_length=64, null=True)
    default_page_description = models.TextField(max_length=256, null=True)
    default_page_keywords = models.TextField(max_length=128, null=True)

    change_theme_light_in_footer = models.BooleanField(default=True)
    change_theme_light_in_navbar = models.BooleanField(default=True)
    change_language_in_navbar = models.BooleanField(default=True)
    change_language_in_footer = models.BooleanField(default=True)

    # Management
    allow_field_translation = models.BooleanField(default=False)
    last_huey_flush = models.DateTimeField(null=True)
    has_user_home = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Submodules
    article_folders = models.ManyToManyField(ArticlesFolder, related_name="+")
    page_folders = models.ManyToManyField(PagesFolder, related_name="+")

    def __str__(self):
        return self.name

    def get_attr_name_for_submodule_folder_model(self, Model):
        if Model == ArticlesFolder:
            return "article_folders"
        if Model == PagesFolder:
            return "page_folders"
        raise SubmoduleFolderModelUnknow(f"The model {Model} is not recodnied in the application.")

    def get_submodule_folders(self, Model):
        attr_name = self.get_attr_name_for_submodule_folder_model(Model)
        submodule_folder_attr = getattr(self, attr_name)
        if submodule_folder_attr:
            return submodule_folder_attr.all()

    def get_submodule_folders_as_list(self, Model):
        objs = self.get_submodule_folders(Model)
        return [f.name for f in objs] if objs else []

    @cached_property
    def url(self):
        schema = "https" if settings.HTTPS else "http"
        return f"{schema}://{self.domain}"

    def get_admin_url_for_model_instance(self, obj):
        # the url to the Django admin form for the model instance
        info = (obj._meta.app_label, obj._meta.model_name)
        return reverse("admin:{}_{}_change".format(*info), args=(obj.pk,))

    def get_full_admin_url_for_model_instance(self, obj):
        return self.url + self.get_admin_url_for_model_instance(obj)

    def get_navbar_links(self, show_types: list):
        return self.navbarlink_set.filter(show_type__in=show_types).distinct()

    def get_footer_items(self, show_types: list):
        return self.footeritem_set.filter(show_type__in=show_types, footerlink__isnull=False).distinct()

    def get_footer_links(self, show_types: list):
        return self.footerlink_set.filter(show_type__in=show_types, footer_item=None).distinct()

    def get_social_media_links(self, show_types: list):
        return self.socialmedialink_set.filter(show_type__in=show_types).distinct()


class Traffic(Model):
    # TODO: check django-request for more attrs
    # https://github.com/django-request/django-request/blob/master/request/models.py
    # Request info
    request_path = models.CharField(max_length=255)
    request_method = models.CharField(default="GET", max_length=7)
    request_GET = models.TextField(null=True)
    request_POST = models.TextField(null=True)
    request_GET_ref = models.CharField(max_length=255, null=True)
    request_headers = models.TextField(null=True)
    request_user = ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    request_country_code = models.CharField(max_length=8, null=True)
    request_site = ForeignKey(Site, blank=True, null=True, on_delete=models.SET_NULL)

    # Response info
    response_code = models.PositiveSmallIntegerField(default=200)
    response_headers = models.TextField(null=True)

    # Others
    time = models.DateTimeField(_("time"), default=timezone.now, db_index=True)

    def __str__(self):
        return f"[{self.time}] {self.request_method} {self.request_path} {self.response_code}"
