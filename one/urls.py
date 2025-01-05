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
    path("🔎/", include("one.search.urls")),
    path("search/", include("one.search.urls")),
    path("📝/", include("one.articles.urls")),
    path("articles/", include("one.articles.urls")),
    path("📚/", include("one.books.urls")),
    path("books/", include("one.books.urls")),
    path("🌐/", include("one.pages.urls")),
    path("pages/", include("one.pages.urls")),
    path("👤/", include("one.users.urls")),
    path("account/", include("one.users.urls")),
    path("🚀/", include("one.plans.urls")),
    path("plans/", include("one.plans.urls")),
    path("🔨/", include("one.tools.urls")),
    path("tools/", include("one.tools.urls")),
    path("🤔/", include("one.faqs.urls")),
    path("faqs/", include("one.faqs.urls")),
    path("💬/", include("one.chat.urls")),
    path("chat/", include("one.chat.urls")),
    path("clients/", include("one.clients.urls")),
    path("englishquizzes/", include("one.quiz.urls")),
    path("", include("one.base.urls")),
    path("", include("one.home.urls")),
] + debug_toolbar_urls()
