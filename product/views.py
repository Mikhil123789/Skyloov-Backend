import threading
from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from product.models import Products
from .serializers import ProductSerializer, ProductSearchSerializer, ProductImageSerializer
from rest_framework import status
from PIL import Image

from .utils import get_products_filter



@api_view(['POST'])
def update_product_image(request, product_id):
    try:
        product = Products.objects.get(pk=product_id)
    except Products.DoesNotExist:
        return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductImageSerializer(data=request.data)
    if serializer.is_valid():
        
        image = serializer.validated_data['image']
        # print(image)
        # import pdb; pdb.set_trace()
        def process_image():
            # Save original image
            product.image = image
            product.save()

        # # Generate and save thumbnail
        # thumbnail_size = (1000, 1000)  # Customize the size according to your needs
        # thumbnail = Image.open(image)
        # thumbnail.thumbnail(thumbnail_size)
        # thumbnail_path = f"thumbnails/{product_id}.jpg"  # Customize the path to save the thumbnail
        # thumbnail.save(thumbnail_path)

        # # Generate and save full-size image
        # full_size_image_path = f"full_size_images/{product_id}.jpg"  # Customize the path to save the full-size image
        # full_size_image = Image.open(image)
        # full_size_image.save(full_size_image_path)

        thread = threading.Thread(target=process_image)
        thread.start()

        return Response({"message": "Product Image Uploaded Successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProductSearchView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=ProductSerializer)
    def get(self, request):
        try:
            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Number of products per page
            name = request.GET.get('name', None)
            sort_by = request.GET.get('sort_by', 'name')
            order_ = request.GET.get('order_by', 'asc')
            if order_ == 'desc':
                sort_by = '-' + sort_by
            products = Products.objects.filter(name__icontains=name).order_by(sort_by)
              #check data available or not
            if not products:
                response_data = {
                'error': "Sorry!,Unable to find any data."
            }
                return Response(response_data, status=status.status.HTTP_404_NOT_FOUND)

            paginated_products = paginator.paginate_queryset(products, request)
            # Serialize the paginated products
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            response_data = {
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ProductFilterView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticated]
    @extend_schema(responses=ProductSearchSerializer)
    def get(self, request):
        try:
            serializer = ProductSearchSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)
            search_criteria = serializer.validated_data
            # product search logic using the search criteria
            filter_objects = Q()
            for key,value in search_criteria.items():
                filter_objects &= get_products_filter(key,value)
            # Pagination
            paginator = PageNumberPagination()
            paginator.page_size = 10  # Number of products per page
            sort_by = request.GET.get('sort_by', 'name')
            order_ = request.GET.get('order_by', 'asc')
            if order_ == 'desc':
                sort_by = '-' + sort_by

            search_results = Products.objects.filter(filter_objects).order_by(sort_by)
            paginated_products = self.paginate_queryset(search_results, request)
        
            # Serialize the paginated products
            serializer = ProductSerializer(paginated_products, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            response_data = {
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


