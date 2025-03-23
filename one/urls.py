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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _

if settings.ENV == "prod":
    # Custom 404 error view
    handler404 = "one.base.views.error_404"
    # Custom 500 error view
    handler500 = "one.base.views.error_500"

urlpatterns = [
    # Django
    path("abcdef/doc/", include("django.contrib.admindocs.urls")),
    path("abcdef/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # Third-party
    path("allauth/", include("allauth.urls")),  # if changes -> check base.html
    path("__reload__/", include("django_browser_reload.urls")),
    # Own
    path(_("search/"), include("one.search.urls")),
    path("articles/", include("one.articles.urls")),
    path("account/", include("one.users.urls")),
    path("plans/", include("one.plans.urls")),
    path("products/", include("one.products.urls")),
    path("tools/", include("one.tools.urls")),
    path("faqs/", include("one.faqs.urls")),
    path("clients/", include("one.clients.urls")),
    path("englishquizzes/", include("one.quiz.urls")),
    path("dgt/", include("one.dgt.urls")),
    path("emails/", include("one.emails.urls")),
    path("etsy/", include("one.etsy.urls")),
    path("", include("one.tex.urls")),
    path("", include("one.base.urls")),
]


if settings.ENV == "dev" and settings.DEBUG:
    urlpatterns = [
        re_path(r"^rosetta/", include("rosetta.urls")),
    ] + urlpatterns
