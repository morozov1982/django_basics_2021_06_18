import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)

    return same_products


def products(request, pk=None, page=1):
    title = 'продукты/каталог'

    basket = get_basket(request.user)

    links_menu = ProductCategory.objects.filter(is_deleted=False)
    products = Product.objects.all().order_by('price')

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)[:3]

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_deleted=False).order_by('price')
            category = {'name': 'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(is_deleted=False, category__pk=pk).order_by('price')

        paginator = Paginator(products, 3)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'hot_product': hot_product,
            'same_products': same_products,
            'category': category,
            'basket': basket,
        }
        return render(request=request, template_name='mainapp/products.html', context=context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': basket,
    }
    return render(request=request, template_name='mainapp/products.html', context=context)


def product(request, pk):
    title = 'продукты'

    links_menu = ProductCategory.objects.filter(is_deleted=False)

    context = {
        'title': title,
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', context)
