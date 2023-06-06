from django.contrib import admin
from .models import Cart, CartItem
# from mptt.admin import MPTTModelAdmin

admin.site.register(CartItem)
admin.site.register(Cart)

