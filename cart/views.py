import traceback
import json
from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializer import CartSerializer, CartItemSerializer
from . import models
from product.models import Products
class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CartSerializer)
    def get(self, request, pk=None):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Number of products per page
        if pk:
            try:
                cart_item = models.Cart.objects.get(pk=pk)
                serializer = CartSerializer(cart_item)
                return Response(serializer.data)
            except models.Cart.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            cart_items = models.Cart.objects.all()
            paginated_products = paginator.paginate_queryset(cart_items, request)
            serializer = CartSerializer(paginated_products, many=True)
            return Response(serializer.data)
    @extend_schema(responses=CartItemSerializer)
    def post(self, request):
        try:
            cart_= models.Cart.objects.get(user=request.user.id)
            data_ = json.loads(request.GET.get('cart_items')) 
            cart_item = list(map(lambda item: {**item, 'cart': cart_.id}, data_))
            serializer = CartItemSerializer(data=cart_item, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Cart created successfully', 'cart': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            response_data = {
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(responses=CartItemSerializer)
    def put(self, request, pk):
        """Update existing cart item quantity"""
        try:
            try:
                cart_ = models.CartItem.objects.filter(pk=pk).first()
                
            except models.CartItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if request.GET.get("type") == "inc":
                    cart_.quantity += 1
            else:
                cart_.quantity -=1
            cart_.save()
        
            # serializer = CartItemSerializer(cart_, many=True)
            return Response( status=status.HTTP_200_OK)
        

        except Exception as e:
            traceback.print_exc()
            response_data = {
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(responses=CartItemSerializer)
    def delete(self, request, pk):
        try:
            cart_item = models.CartItem.objects.get(pk=pk)
        except models.CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response({"message":"Successfully removed the cart item"},status=status.HTTP_204_NO_CONTENT)
