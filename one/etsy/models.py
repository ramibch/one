from auto_prefetch import ForeignKey, Model
from django.db import models


class Shop(Model):
    pass


class Listing(Model):
    shop = ForeignKey(Shop, on_delete=models.CASCADE)
