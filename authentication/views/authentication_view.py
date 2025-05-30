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
        
class RegisterUserView(APIView):
    """
    API View for user registration. Accessible by any user (open endpoint).
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request to register a new user.
        """
        try:
            email = request.data.get('email')
            name = request.data.get('name')
            password = request.data.get('password')

            # Validate required fields
            if not email or not name or not password:
                return Response({
                    'status': False,
                    'message': 'Email, name, and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({
                    'status': False,
                    'message': 'Email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create the user using UserManager
            user = User.objects.create_user(
                email=email,
                name=name,
                password=password
            )

            # Serialize the user data for response
            serializer = UserSerializer(user)

            return Response({
                'status': True,
                'message': 'User registered successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Handle validation errors (e.g., invalid email)
            return Response({
                'status': False,
                'message': 'Validation error',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred during registration',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class CreateSuperuserView(APIView):
    """
    API View for creating a superuser. Accessible only by admin users.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request to create a new superuser.
        """
        try:
            email = request.data.get('email')
            name = request.data.get('name')
            password = request.data.get('password')

            # Validate required fields
            if not email or not name or not password:
                return Response({
                    'status': False,
                    'message': 'Email, name, and password are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({
                    'status': False,
                    'message': 'Email already exists'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create the superuser using UserManager
            user = User.objects.create_superuser(
                email=email,
                name=name,
                password=password
            )

            # Serialize the user data for response
            serializer = UserSerializer(user)

            return Response({
                'status': True,
                'message': 'Superuser created successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Handle validation errors (e.g., invalid email, is_staff/is_superuser issues)
            return Response({
                'status': False,
                'message': 'Validation error',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred during superuser creation',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)