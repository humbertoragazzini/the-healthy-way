from django.shortcuts import render, get_object_or_404
from .models import Product, Plans, TypeOfPlan

# Create your views here.


def all_products(request):
    """ view to show all product sorting and search queries"""

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ view to show product detail and if is a plan, show duration"""

    product = get_object_or_404(Product, pk=product_id)
    type_of_plan = False
    
    try:
        plan = get_object_or_404(Plans, name=product.pk)
        type_of_plan = get_object_or_404(TypeOfPlan, name=plan.kind_of_plan)
    except:
        plan = False

    context = {
        'product': product,
        'plan': plan,
        'type_of_plan': type_of_plan,
    }

    return render(request, 'products/product_detail.html', context)