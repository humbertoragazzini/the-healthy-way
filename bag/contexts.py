""" Contexts variables and def """
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Category


def bag_contents(request):
    """ Shoppig bag + limited quantity of plans cuantity and delivery """
    bag_items = []
    total_count = 0
    total = 0
    product_count = 0
    category = get_object_or_404(Category, name='nutrition_and_workout_plans')
    delivery = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in bag.items():
        total_count+=quantity
        product = get_object_or_404(Product, pk=item_id)
        if product.category != category:
            total += quantity * product.price
            product_count += quantity
            delivery = total * Decimal(
                settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            total += product.price

        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    grand_total = delivery + total

    context = {
        'total_count': total_count,
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
