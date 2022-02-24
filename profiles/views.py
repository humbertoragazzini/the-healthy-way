from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from products.models import Plans, Product, Category

from checkout.models import Order

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    plans = Plans.objects.all()
    cache_plans = []
    cache_items = []
    plan_category = Category.objects.get(name='nutrition_and_workout_plans')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Profile could not be save')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    for order in orders:
        for item in order.lineitems.all():
            if item.product not in cache_items:
                cache_items.append(item.product)
                cache_product = Product.objects.get(name=item.product.name)
                if cache_product.category.name == plan_category.name:
                    cache=plans.filter(name=cache_product.pk)
                    cache_plans.append(cache[0])
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'plans': cache_plans,
    }

    return render(request, template, context)
@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)