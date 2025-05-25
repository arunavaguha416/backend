from django.urls import path
from authentication.views.authentication_view import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]