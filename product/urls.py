from django.urls import path
from .views import ProductSearchView, ProductFilterView, update_product_image

urlpatterns = [
    
    path('search/', ProductSearchView.as_view(), name='search_products'),
    path('filter/', ProductFilterView.as_view(), name='filter products'),
    path('upload-image/<int:product_id>/', update_product_image, name='upload_product_image'),
    
]