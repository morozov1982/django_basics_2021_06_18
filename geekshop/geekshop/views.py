from django.shortcuts import render
from mainapp.models import Product


def index(request):
    title = 'магазин'

    products = Product.objects.all()[:3]

    context = {
        'title': title,
        'products': products,
    }
    return render(request=request, template_name='geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
    }
    return render(request=request, template_name='geekshop/contact.html', context=context)
