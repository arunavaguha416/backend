from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.db.models import Q
from authentication.serializers.user_serializer import *
from django.core.paginator import Paginator
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    """
    API View for user login. Accessible by any user.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request to authenticate a user and return a token.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            if not email or not password:
                return Response({
                    'status': False,
                    'message': 'Email and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(email=email, password=password)
            if user:
                # Generate token for authenticated user
                token = RefreshToken.for_user(user)
                return Response({
                    'status': True,
                    'message': 'Login successful',
                    'token': str(token),
                    'access': str(token.access_token),
                    'user' : user.id,
                }, status=status.HTTP_200_OK)

            return Response({
                'status': False,
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred during login',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)