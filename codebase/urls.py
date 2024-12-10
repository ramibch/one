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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Custom 404 error view
handler404 = "codebase.base.views.error_404"
# Custom 500 error view
handler500 = "codebase.base.views.error_500"

urlpatterns = [
    # Django
    path("abcdef/doc/", include("django.contrib.admindocs.urls")),
    path("abcdef/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # Third-party
    path("allauth/", include("allauth.urls")),  # if changes -> check base.html
    path("__reload__/", include("django_browser_reload.urls")),
    # Own
    path("🔎/", include("codebase.search.urls")),
    path("📝/", include("codebase.articles.urls")),
    path("🌐/", include("codebase.pages.urls")),
    path("👤/", include("codebase.users.urls")),
    path("🚀/", include("codebase.plans.urls")),
    path("🔨/", include("codebase.tools.urls")),
    path("🤔/", include("codebase.faqs.urls")),
    path("💬/", include("codebase.chat.urls")),
    path("", include("codebase.base.urls")),
    path("", include("codebase.home.urls")),
] + debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
