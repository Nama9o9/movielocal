
from django.contrib import admin
from .models import ShoppingCart, ShoppingCartItem, Payment

# Register your models here.
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Payment)