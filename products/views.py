from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator

import random

# Create your views here.
# def latest_prod():
#     lat_pag = Paginator(latest_products, 1)
#
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None): #category_slug нужен для создания url категории
    # If categories don't exist, it must be None
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    latest_products = Product.objects.order_by('name')[:3]

    if category_slug: #если наш slug не пустой и пользователь выбрал какую то категорию
        category = get_object_or_404(Category, slug=category_slug) #берём каьегорию по слагу
        products = products.filter(category=category) #берём все продукты с данной категории

    paginator = Paginator(products, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next = '?page={}'.format(page.next_page_number())
    else:
        next = ''

    context = {
        'category': category,
        'categories': categories,
        'products': page,
        'latest_products': latest_products,
        'is_paginated': is_paginated,
        'next': next,
        'prev_url': prev_url,
        }
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id, status=True)
    latest_products = Product.objects.order_by('name')[:3]
    categories = Category.objects.all()


    category_products=Product.objects.filter(category=product.category)
    random_products = random.choices(category_products, k=3)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'random_products': random_products,
        'latest_products': latest_products,
        'categories': categories,
        'cart_product_form': cart_product_form


    }
    return render(request, 'product_detail.html', context)
