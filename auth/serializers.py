from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token
    
class MyTokenQuerySerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
class MyTokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    
class MyTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    
class MyTokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    access = serializers.CharField(required=True)