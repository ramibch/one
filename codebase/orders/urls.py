from django.urls import path

from .views import stripe_webhook
from .views import checkout
from .views import order_detail
from .views import order_invoice

urlpatterns = [
    path("stripe/webhook/", stripe_webhook, name="webhook-intent"),
    path("checkout/<int:id>/", checkout, name="product-checkout"),
    path("<uuid:uuid>/", order_detail, name="order-detail"),
    path("<uuid:uuid>/invoice/", order_invoice, name="order-invoice"),
]
