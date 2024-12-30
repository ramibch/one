from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SearchTerm(Model):
    query = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    client = ForeignKey("clients.Client", null=True, on_delete=models.SET_NULL)
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    site = ForeignKey("sites.Site", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.query
