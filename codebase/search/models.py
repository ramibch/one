from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SearchTerm(Model):
    query = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = ForeignKey(User, null=True, on_delete=models.SET_NULL)
    country_code = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.query
