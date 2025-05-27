from django.urls import path
from authentication.views.authentication_view import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('create-super-user/', CreateSuperuserView.as_view(), name='superuser'),
    
]