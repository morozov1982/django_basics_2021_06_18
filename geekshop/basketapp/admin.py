from django.contrib import admin
from basketapp.models import Basket

# admin.site.register(Basket)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'quantity',
        'add_datetime',
    ]
