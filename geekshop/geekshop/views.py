from django.shortcuts import render


def index(request):
    title = 'магазин'
    context = {
        'title': title,
    }
    return render(request=request, template_name='geekshop/index.html', context=context)


def contacts(request):
    title = 'контакты'
    context = {
        'title': title,
    }
    return render(request=request, template_name='geekshop/contact.html', context=context)
