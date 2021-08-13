from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product

from django.contrib.auth.decorators import login_required


@login_required
def basket(request):
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).order_by('product__category').select_related()
        context = {
            'basket': basket
        }
        return render(request, 'basketapp/basket.html', context)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            if quantity < new_basket_item.quantity or new_basket_item.product.quantity:
                new_basket_item.quantity = quantity
                new_basket_item.save()
        else:
            new_basket_item.delete()

        basket = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

        context = {
            'basket': basket,
        }

        product_price = new_basket_item.product.price * new_basket_item.quantity

        # result = render_to_string('basketapp/includes/inc_basket_list.html', context)
        result = render_to_string('basketapp/includes/inc_basket_summary.html', context)

        return JsonResponse({'result': result, 'product_price': product_price})
