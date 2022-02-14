""" All views of bag app """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from products.models import Product, Category


def view_bag(request):
    """ view to return de bag page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    product = Product.objects.get(pk=item_id)
    category = Category.objects.get(name='nutrition_and_workout_plans')

    if item_id in list(bag.keys()):
        if product.category == category:
            messages.error(request, 'Sorry you can add the same plan two times')
            redirect(redirect_url)
        else:
            bag[item_id] += quantity
            messages.success(request, f'Added {product.name} to your bag')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def remove_item_bag(request, item_id):
    """ Remove product to the shopping bag """

    bag = request.session.get('bag', {})
    print(bag[item_id])

    if bag[item_id] > 0:
        bag[item_id] = bag[item_id]-1
        if bag[item_id] == 0:
            del bag[item_id]

    request.session['bag'] = bag

    print(bag)

    return redirect(reverse(view_bag))
