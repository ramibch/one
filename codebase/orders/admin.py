from django.contrib import admin


from .models import ProductOrder, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ("address_country",)

    list_display = ("email", "name", "address_city", "address_country")


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_filter = ("product", "customer", "created_on")
    list_display = ("__str__", "uuid", "created_on", "product", "customer")
    readonly_fields = (
        "uuid",
        "product",
        "customer",
        "checkout_payload",
        "invoice_payload",
        "payment_intent",
        "event_id",
        "invoice_id",
        "invoice_pdf",
    )
