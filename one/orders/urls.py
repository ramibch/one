from django.urls import path

from .views import checkout, order_detail, order_invoice, stripe_webhook

urlpatterns = [
    path("stripe/webhook/", stripe_webhook, name="webhook-intent"),
    path("checkout/<int:id>/", checkout, name="product-checkout"),
    path("<uuid:uuid>/", order_detail, name="order-detail"),
    path("<uuid:uuid>/invoice/", order_invoice, name="order-invoice"),
]
