from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    title = 'магазин'

    # products = Product.objects.all()[:3]
    products = Product.objects.filter(is_deleted=False, category__is_deleted=False)[:3]

    context = {
        'title': title,
        'products': products,
    }
    return render(request=request, template_name='geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'title': title,
        'basket': basket,
    }
    return render(request=request, template_name='geekshop/contact.html', context=context)
