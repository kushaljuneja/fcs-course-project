import logging
import urllib
import json
from account.models import UserBase
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from orders.models import Order
from store.models import Product

from .forms import AddCategoryForm, AddProductForm, SellerRegistrationForm

db_logger = logging.getLogger('db')


@login_required
def seller_home(request):
    orders = Order.objects.all()
    return render(request, 'seller/seller_home.html', {'orders': orders})


@login_required
def become_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = UserBase.objects.get(pk=request.user.pk)
            user.verification_document = request.FILES['verification_document']
            user.user_type = 2  # make user as unverified seller
            user.save()
            messages.info(
                request, f'Your seller application has been sent to the Admin for approval')
            return redirect('store:store_home')
    else:
        form = SellerRegistrationForm()

    return render(request, 'seller/become_seller_form.html', {'form': form})


@login_required
def show_products(request):
    products = Product.objects.filter(created_by__id=request.user.id)
    return render(request, 'seller/show_products.html', {'products': products})


@login_required
def add_product(request):
    user = request.user
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                product = form.save(commit=False)
                product.created_by = request.user
                product.save()
                messages.success(
                    request, f'Product {product.title} added successfully!')
                db_logger.info(
                    f"User: {user.user_name}, added product: {product.title}")
                return redirect('seller:seller_home')
            else:
                messages.warning(
                    request, 'Invalid reCAPTCHA. Please try again.')
                return redirect(reverse('seller:add_product'))

    else:
        form = AddProductForm()

    return render(request, 'seller/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                form.save()
                messages.success(
                    request, f'You have edited details of {product.title}')
                db_logger.info(
                    f"User: {request.user.user_name}, edited product: {product.title}")
                return redirect('seller:seller_home')
            else:
                messages.warning(
                    request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'seller/edit_product.html', {'form': form})
    else:
        form = AddProductForm(instance=product)

    return render(request, 'seller/edit_product.html', {'form': form})


@login_required
def add_category(request):
    user = request.user
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                category = form.save(commit=False)
                category.name = form.cleaned_data['name']
                category.save()
                messages.success(request, f'Added new category: {category.name}')
                db_logger.info(
                    f"User: {user.user_name}, added category: {category.name}")
                return redirect('seller:seller_home')
            else:
                messages.warning(
                    request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'seller/add_category.html', {'form': form})

    else:
        form = AddCategoryForm()

    return render(request, 'seller/add_category.html', {'form': form})
