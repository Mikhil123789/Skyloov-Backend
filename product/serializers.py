from rest_framework import serializers
from . import models

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brands
        fields = "__all__"
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"



class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    # image_url = serializers.Chara()
    class Meta:
        model = models.Products
        fields = ['id', 'name', 'price', 'description','brand','category', 'image']
    # def get_image_url(self, obj):
    #     if obj.image:
    #         return self.context['request'].build_absolute_uri(obj.image.url)
    #     return None

 

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