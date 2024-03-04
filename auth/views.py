from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from .serializers import MyTokenObtainPairSerializer

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class MyTokenVerifyView(TokenVerifyView):
    pass