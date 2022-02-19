# webhooks
"""webhooks handlers"""
from django.http import HttpResponse
from products.models import Product

import json
import time


class StripeWH_Handler:
    """
    handle stripe webhook
    """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        handle generic /unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200,)

    def handle_payment_intent_succeeded(self, event):
        """
        handle the payment_intent.succeeded webhook
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.data.charges[0].amount / 100, 2)

        #clean al data
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        order_exists = False
        attempt = 1
        while attempt <= 5:
                
            try:
                order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        email__iexact=billing_details.email,
                        phone_number__iexact=shipping_details.phone,
                        country__iexact=shipping_details.country,
                        postcode__iexact=shipping_details.postal_code,
                        town_or_city__iexact=shipping_details.city,
                        street_address1__iexact=shipping_details.line1,
                        street_address2__iexact=shipping_details.line2,
                        county__iexact=shipping_details.state,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
                
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.country,
                    postcode=shipping_details.postal_code,
                    town_or_city=shipping_details.city,
                    street_address1=shipping_details.line1,
                    street_address2=shipping_details.line2,
                    county=shipping_details.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200,)

    def handle_payment_intent_payment_failed(self, event):
        """
        handle the payment_intent.failed webhook
        """
        print("fallo el pago//////////////")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,)
