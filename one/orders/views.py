import json

import stripe
from content.models import ListingProduct
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from utils.telegram import report_to_admin

from .models import Customer, ProductOrder

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(request, product: ListingProduct):
    """
    Creates and returns a Stripe Checkout Session
    """

    order = ProductOrder.objects.create(product=product)

    success_url = request.build_absolute_uri(
        order.success_checkout_url + "?session_id={CHECKOUT_SESSION_ID}"
    )

    cancel_url = request.build_absolute_uri(
        order.cancel_checkout_url + "?session_id={CHECKOUT_SESSION_ID}"
    )

    # example of how to insert the SUBSCRIBER_CUSTOMER_KEY: id in the metadata
    # to add customer.subscriber to the newly created/updated customer.
    metadata = {"product_id": product.id, "order_id": order.id}

    session = stripe.checkout.Session.create(
        payment_method_types=["sepa_debit", "card"],  # "paypal",
        # payment_method_types[0]:
        # must be one of card, acss_debit, affirm, afterpay_clearpay,
        # alipay, au_becs_debit, bacs_debit, bancontact, blik, boleto,
        # cashapp, customer_balance, eps, fpx, giropay, grabpay, ideal,
        # klarna, konbini, link, oxxo, p24, paynow, paypal, pix,
        # promptpay, sepa_debit, sofort, us_bank_account, wechat_pay, or zip
        # payment_method_types=["bacs_debit"],  # for bacs_debit
        payment_intent_data={
            "setup_future_usage": "off_session",
            # so that the metadata gets copied to
            # the associated Payment Intent and Charge Objects
            "metadata": metadata,
        },
        line_items=[
            {
                "price_data": {
                    "currency": "eur",  # for bacs_debit
                    "unit_amount": product.price_in_cents,
                    "tax_behavior": "inclusive",
                    "product_data": {
                        "name": product.title,
                        "images": [product.image.url],
                    },
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        invoice_creation={"enabled": True},
        automatic_tax={"enabled": True},
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
    )

    return session


def checkout(request, id):  # pragma: no cover
    product = get_object_or_404(ListingProduct, id=id)
    checkout_session = create_stripe_session(request, product)
    return redirect(checkout_session.url, code=303)


@csrf_exempt
def stripe_webhook(request):  # pragma: no cover
    payload = request.body
    sig_header = request.headers["stripe-signature"]
    event = None
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        print("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        print("Invalid signature")
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Retrieve the session. If you require line items in the response,
        # you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event["data"]["object"]["id"],
            expand=["line_items"],
        )
        _ = session.line_items

        data = json.loads(payload)

        # with open(settings.BASE_DIR / "stripe.txt", "wb") as f:
        #    f.write(payload)
        metadata = data["data"]["object"]["metadata"]
        if "product_id" not in metadata or "order_id" not in metadata:
            # another site
            report_to_admin(
                f"Stripe Webhook from another site:\n\n{str(data['data']['object'])}"
            )
            return HttpResponse(status=200)

        product_id = metadata["product_id"]
        order_id = metadata["order_id"]

        event_id = data["id"]
        invoice_id = data["data"]["object"]["invoice"]
        payment_intent = data["data"]["object"]["payment_intent"]
        name = data["data"]["object"]["customer_details"]["name"]
        email = data["data"]["object"]["customer_details"]["email"]
        address_city = data["data"]["object"]["customer_details"]["address"]["city"]
        address_country = data["data"]["object"]["customer_details"]["address"][
            "country"
        ]
        address_line1 = data["data"]["object"]["customer_details"]["address"]["line1"]
        address_line2 = data["data"]["object"]["customer_details"]["address"]["line2"]
        address_postal_code = data["data"]["object"]["customer_details"]["address"][
            "postal_code"
        ]
        address_state = data["data"]["object"]["customer_details"]["address"]["state"]

        # Get the order
        order = ProductOrder.objects.get(id=order_id)

        # Get the product
        product = ListingProduct.objects.get(id=product_id)

        #
        customer = Customer.objects.create(
            name=name,
            email=email,
            address_city=address_city,
            address_country=address_country,
            address_line1=address_line1,
            address_line2=address_line2,
            address_postal_code=address_postal_code,
            address_state=address_state,
        )
        order.event_id = event_id
        order.invoice_id = invoice_id
        order.payment_intent = payment_intent
        order.checkout_payload = str(data)
        order.customer = customer
        order.save()
        if order.customer is not None:
            order.send_email()
            report_to_admin(
                f"💸 {name} '{email}' ordered the product '{product.title}'"
            )

    # Passed signature verification
    return HttpResponse(status=200)


@never_cache
def order_detail(request, uuid):
    obj = get_object_or_404(ProductOrder, uuid=uuid)
    if obj.has_expired():
        return render(request, "product_order_expired.html")
    return render(request, "product_order.html", {"object": obj})


@never_cache
def order_invoice(request, uuid):
    obj = get_object_or_404(ProductOrder, uuid=uuid)
    if not obj.invoice_pdf:
        ## view for getting invoice from stripe
        ## https://stripe.com/docs/api/invoices/retrieve?lang=python
        r = stripe.Invoice.retrieve(obj.invoice_id)
        obj.invoice_payload = str(json.dumps(r))
        obj.invoice_pdf = r["invoice_pdf"]
        obj.save()
    return HttpResponseRedirect(obj.invoice_pdf)
