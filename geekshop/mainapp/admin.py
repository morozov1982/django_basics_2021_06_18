from django.contrib import admin
from ordersapp.models import Order
from .models import ProductCategory, Product

admin.site.register(ProductCategory)
# admin.site.register(Product)
admin.site.register(Order)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'quantity',
        'created_at',
    ]
