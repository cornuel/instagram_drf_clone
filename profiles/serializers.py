from rest_framework import serializers
from .models import Profile


class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'full_name',
            'profile_pic'
        )


class PublicProfileSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_following_count(self, obj: Profile):
        return obj.follows.count()

    def get_followers_count(self, obj: Profile):
        return obj.followed_by.count()

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'full_name',
            'bio',
            'profile_pic',
            'following_count',
            'followers_count',
        )


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'full_name',
            'bio',
            'profile_pic',
            'follows'
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    favorite_posts = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        read_only=True
    )
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_following_count(self, obj: Profile):
        return obj.follows.count()

    def get_followers_count(self, obj: Profile):
        return obj.followed_by.count()

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'full_name',
            'bio',
            'profile_pic',
            'favorite_posts',
            'following_count',
            'followers_count',
            'created_at',
            'updated_at'
        )

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
