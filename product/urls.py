from django.urls import path
from .views import ProductSearchView, ProductFilterView

urlpatterns = [
    
    path('search/', ProductSearchView.as_view(), name='search_products'),
    path('filter/', ProductFilterView.as_view(), name='filter products')
    
]