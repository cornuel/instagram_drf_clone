from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import re


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    url = serializers.HyperlinkedIdentityField(
        many=False, view_name='profiles-detail', lookup_field='username')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'url')
        lookup_field = 'username'

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_password(self, value):
        """
        Validate whether the password is strong enough.
        """
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                "Password must contain at least one number.")
        if not re.search(r'\W', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character.")
        return value
