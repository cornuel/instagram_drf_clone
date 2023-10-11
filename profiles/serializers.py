from rest_framework import serializers
from .models import Profile


class PublicProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'bio', 'image')
        
class ProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'bio', 'image', 'follows')

class ProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    bio = serializers.CharField(required=False)
    image = serializers.URLField(required=False)
    favorite_posts = serializers.SlugRelatedField(
        many=True, 
        slug_field='slug', 
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ('id', 'username', 'bio', 'image','favorite_posts', 'follows', 'created_at', 'updated_at')

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance