"""Views of products app"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Plans, TypeOfPlan, Category
from .forms import ProductForm, PlansForm

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
        try:
            plan = Plans.objects.get(name=product.pk)
            type_of_plan = get_object_or_404(TypeOfPlan, name=plan.kind_of_plan)
        except Plans.DoesNotExist:
            plan = False
            type_of_plan = None

    else:
        type_of_plan = None
        plan = False

    context = {
        'product': product,
        'plan': plan,
        'type_of_plan': type_of_plan,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    plan = get_object_or_404(Category, name='nutrition_and_workout_plans')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_plan = Product.objects.filter(name=form.save())
            if product_plan[0].category.id == plan.id:
                product_id = product_plan[0].id
                print(product_id)
                return redirect(reverse('add_plan',args=[product_id]))
            else:
                messages.success(request, 'Successfully added product!')
                return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def add_plan(request, product_id):
    """ Link plan to product """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    plan = None
    print(product)
    if request.method == 'POST':
        form = PlansForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Link Successfully')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to link the plan. Please ensure the form is valid.')
    else:
        try:
            plan = Plans.objects.get(name=product.pk)
            form = PlansForm(instance=plan)
        except Plans.DoesNotExist:
            form = PlansForm()

    template = 'products/add_plan.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    plan = get_object_or_404(Category, name='nutrition_and_workout_plans')
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_plan = Product.objects.filter(name=form.save())
            if product_plan[0].category.id == plan.id:
                product_id = product_plan[0].id
                return redirect(reverse('add_plan',args=[product_id]))
            else:
                messages.success(request, 'Successfully updated product!')
                return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)    

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)

    plan = get_object_or_404(Category, name='nutrition_and_workout_plans')

    try:
        plan = Plans.objects.get(name=product.pk)
        plan.delete()
        product.delete()
    except Plans.DoesNotExist:
        product.delete()

    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))