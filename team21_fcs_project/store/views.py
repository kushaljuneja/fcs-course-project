from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Category, Product
from django.conf import settings
from django.contrib.auth.decorators import login_required

def get_in_stock_products():
    products = Product.objects.filter(is_active=True, in_stock=True)
    return products

def product_all(request):
    products = get_in_stock_products()
    return render(request, 'store/index.html', {'products': products})


def category_list(request, pk):
    category = Category.objects.get(pk=pk)
    products = get_in_stock_products().filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})

@login_required
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'store/single.html', {'product': product, 'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY})


def search_products(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        # we want to search products
        products = get_in_stock_products().filter(Q(title__contains=searched) | Q(category__name__contains=searched))
        # we always have to render something
        return render(request, 'store/search_products.html', {
            'searched': searched, 
            'products': products
        })

    # we always have to render something
    return render(request, 'store/search_products.html', {})

def categories(request):
    return {'categories': Category.objects.all()}
