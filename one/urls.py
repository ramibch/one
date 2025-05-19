"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

if settings.ENV == settings.PROD:
    handler403 = "one.base.views.error_403"
    # Custom 404 error view
    handler404 = "one.base.views.error_404"
    # Custom 500 error view
    handler500 = "one.base.views.error_500"

urlpatterns = [
    # Django
    path("abcdef/doc/", include("django.contrib.admindocs.urls")),
    path("abcdef/", admin.site.urls, name="one_admin"),
    path("i18n/", include("django.conf.urls.i18n")),
    # Third-party
    path("allauth/", include("allauth.urls")),  # if changes -> check base.html
    # Own
    path("account/", include("one.users.urls")),
    path("tools/", include("one.tools.urls")),
    path("englishquizzes/", include("one.quiz.urls")),
    path("quiz/", include("one.quiz.urls")),
    path("dgt/", include("one.dgt.urls")),
    path("emails/", include("one.emails.urls")),
    path("etsy/", include("one.etsy.urls")),
    path("pins/", include("one.pins.urls")),
    path("faqs/", include("one.faqs.urls")),
    path(_("plans/"), include("one.plans.urls")),
    path(_("articles/"), include("one.articles.urls")),
    path(_("products/"), include("one.products.urls")),
    path(_("companies/"), include("one.companies.urls")),
    path("", include("one.tex.urls")),
    path("", include("one.base.urls")),
]


if settings.ENV == settings.DEV and settings.DEBUG:
    urlpatterns = (
        [
            path("rosetta/", include("rosetta.urls")),
            path("__reload__/", include("django_browser_reload.urls")),
        ]
        + debug_toolbar_urls()
        + urlpatterns
    )
