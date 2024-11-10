from django.utils.translation import gettext_lazy as _

# Django urls paths available for links

DJANGO_URL_PATHS = (
    ("home", _("Home")),
    ("search", _("Search")),
    ("sitemap", _("Sitemap")),
    ("article_list", _("Articles")),
    ("plan_list", _("Plans")),
    ("account_login", _("Sign In")),
    ("account_signup", _("Sign Up")),
    ("user_dashboard", _("Account")),
)

# Link show attribute (Link Models)

SHOW_CHOICES = (
    ("user", "👤 " + _("For logged user")),
    ("no_user", "🕵🏻 " + _("For anonymous user")),
    ("always", "👁️ " + _("Show always")),
    ("never", "🫣 " + _("Never show")),
)
