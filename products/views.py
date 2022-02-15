"""Views of products app"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Plans, TypeOfPlan, Category

# Create your views here.


def all_products(request):
    """ view to show all product sorting and search queries"""
    
    products = Product.objects.all()
    query = None
    nbar = 'products'
    direction = None
    plans = Plans.objects.all().select_related(
        'name').select_related('kind_of_plan')

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            nbar = request.GET['category']

            if 'sort' in request.GET:
                sortkey = request.GET['sort']
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You did't enter any search")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'nbar_category': nbar,
        'plans': plans,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ view to show product detail and if is a plan, show duration"""
    product = get_object_or_404(Product, pk=product_id)
    type_of_plan = False
    plan_or_not = Category.objects.filter(name='nutrition_and_workout_plans')
    plan = False

    if plan_or_not[0] == product.category:
        print("hola")
        plan = get_object_or_404(Plans, name=product.pk)
        type_of_plan = get_object_or_404(TypeOfPlan, name=plan.kind_of_plan)

    else:
        type_of_plan = None
        plan = False

    context = {
        'product': product,
        'plan': plan,
        'type_of_plan': type_of_plan,
    }

    return render(request, 'products/product_detail.html', context)
