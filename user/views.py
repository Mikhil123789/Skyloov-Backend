from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken




class UserRegistrationView(APIView):
    """Register skyloov user her."""
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.GET)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({ 'token': token, 'message':'User created successfully' }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'error': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)