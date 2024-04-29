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
    is_following = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    
    def get_is_following(self, obj: Profile) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followed_by.filter(id=request.user.profile.id).exists()
        return False

    def get_following_count(self, obj: Profile) -> int:
        return obj.follows.count()

    def get_followers_count(self, obj: Profile) -> int:
        return obj.followed_by.count()
    
    def get_posts_count(self, obj: Profile) -> int:
        return obj.posts.filter(is_private=False).count()

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'full_name',
            'bio',
            'profile_pic',
            'posts_count',
            'is_following',
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
    posts_count = serializers.SerializerMethodField()

    def get_following_count(self, obj: Profile) -> int:
        return obj.follows.count()

    def get_followers_count(self, obj: Profile) -> int:
        return obj.followed_by.count()
    
    def get_posts_count(self, obj: Profile) -> int:
        return obj.posts.filter(is_private=False).count()

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'full_name',
            'bio',
            'profile_pic',
            'posts_count',
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
