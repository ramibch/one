from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from one.db import OneModel

LINKEDIN_APP = settings.SOCIALACCOUNT_PROVIDERS["linkedin_oauth2"]["APP"]
# LINKEDIN_APP = {'client_id': '', 'secret': '', 'key': ''}


class LinkedinAuthorType(models.TextChoices):
    PERSON = "person", _("Person")
    ORGANIZATION = "organization", _("Organization")


class LinkedinChannel(OneModel):
    name = models.CharField(max_length=64)
    author_type = models.CharField(max_length=32, choices=LinkedinAuthorType)
    token = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


#############################
## Authorization Code Flow ##
#############################

# 1. Configure your application in the Developer Portal
# to obtain Client ID and Client Secret.

# 2. Your application directs the browser to LinkedIn's OAuth 2.0
# authorization page where the member authenticates.

# 3. After authentication, LinkedIn's authorization server passes
# an authorization code to your application.

# 4. Your application sends this code to LinkedIn and LinkedIn returns an access token.

# 5. Your application uses this token to make API calls on behalf of the member.
