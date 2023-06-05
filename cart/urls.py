from django.urls import path
from .views import CartItemAPIView

urlpatterns = [
    path('cart-items/', CartItemAPIView.as_view()),
    path('cart-items/<int:pk>/', CartItemAPIView.as_view()),
]