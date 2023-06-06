from rest_framework import serializers
from . import models



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = "__all__"
 

class ProductSearchSerializer(serializers.Serializer):
    category = serializers.CharField(required=False)
    brand = serializers.CharField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    min_quantity = serializers.IntegerField(required=False)
    max_quantity = serializers.IntegerField(required=False)
    created_at = serializers.DateTimeField(required=False)

    def validate(self, data):
        min_price = data.get('min_price')
        max_price = data.get('max_price')

        if min_price is not None and max_price is not None and max_price < min_price:
            raise serializers.ValidationError("max_price must be greater than or equal to min_price")

        return data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products
        fields = ('image',)