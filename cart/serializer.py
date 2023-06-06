from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Products


class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['id', 'product','quantity', 'created_at','cart']

   
        

class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id','user','cart_item']

  
