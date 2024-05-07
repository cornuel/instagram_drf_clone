from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .serializers import MyTokenObtainPairSerializer, MyTokenResponseSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import MyTokenQuerySerializer
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


@extend_schema(
    summary='Obtain JSON Web Token pair',
    examples=[
        OpenApiExample(
            'Example 1',
            media_type='application/json',
            summary='Log-in with demo account',
            description='Log-in with demo account',
            request_only=True,
            value={
                'username': 'demo',
                'password': '!Rootroot1',
            },
        ),
        OpenApiExample(
            'Example 1',
            media_type='application/json',
            summary='Valid credentials',
            response_only=True,
            status_codes=[200],
            value={
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
            },
        ),
        OpenApiExample(
            'Example 1',
            media_type='application/json',
            summary='Invalid credentials',
            response_only=True,
            status_codes=[401],
            value={
                "detail": "No active account found with the given credentials"
            },
        ),
    ],
    tags=['Authentication'],
    description='Obtains both an access and refresh JSON web token pair. Access Token lasts 10 minutes and Refresh Token lasts a week.',
    responses={
        200: MyTokenResponseSerializer,
        401: 'Your Response Serializer Here'
    },
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
@extend_schema(
    summary='Refresh JSON Web Token',
    tags=['Authentication'],
    description='Refresh your access JSON web token.',
)
class MyTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(
    summary='Verify JSON Web Token',
    tags=['Authentication'],
    description='Verify your access JSON web token.',
    examples=[
        OpenApiExample(
            'Example 1',
            media_type='application/json',
            summary='Valid Token',
            # description='Log-in with demo account',
            response_only=True,
            status_codes=[200],
            value={},
        ),
        OpenApiExample(
            'Example 1',
            media_type='application/json',
            summary='Invalid Token',
            response_only=True,
            status_codes=[401],
            value={
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            },
        ),
    ],
    responses={
        200: 'Your Response Serializer Here',
        401: 'Your Response Serializer Here'
    },
)
class MyTokenVerifyView(TokenVerifyView):
    pass