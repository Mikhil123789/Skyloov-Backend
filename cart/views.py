from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from .serializer import CartSerializer, CartItemSerializer
from . import models

class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CartItemSerializer)
    def get(self, request, pk=None):
        if pk:
            try:
                cart_item = models.CartItem.objects.get(pk=pk)
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data)
            except models.CartItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            cart_items = models.CartItem.objects.all()
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
    @extend_schema(responses=CartItemSerializer)
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @extend_schema(responses=CartItemSerializer)
    def put(self, request, pk):
        try:
            cart_item = models.CartItem.objects.get(pk=pk)
        except models.CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=CartItemSerializer)
    def delete(self, request, pk):
        try:
            cart_item = models.CartItem.objects.get(pk=pk)
        except models.CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
