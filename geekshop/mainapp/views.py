from django.shortcuts import render
from mainapp.models import Product, ProductCategory


def products(request):
    title = 'продукты/каталог'

    categories = ProductCategory.objects.all()

    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    products = Product.objects.all()[:3]
    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
        'categories': categories,
    }
    return render(request=request, template_name='mainapp/products.html', context=context)
