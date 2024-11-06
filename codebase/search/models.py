from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models

User = get_user_model()


class SearchTerm(Model):
    query = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=8, null=True)
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    site = ForeignKey(Site, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.query
