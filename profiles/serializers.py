from rest_framework import serializers
from .models import Profile


class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "username", "full_name", "profile_pic")


class FollowResponseSerializer(serializers.Serializer):
    message = serializers.CharField(required=False)


class PublicProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    def get_username(self, obj: Profile) -> str:
        return obj.username

    def get_is_following(self, obj: Profile) -> bool:
        request = self.context.get("request")
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
            "id",
            "username",
            "full_name",
            "bio",
            "profile_pic",
            "posts_count",
            "is_following",
            "following_count",
            "followers_count",
        )


class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "bio",
            "profile_pic",
            "follows",
        )


class ProfileDetailSerializer(PublicProfileSerializer):

    favorite_posts = serializers.SlugRelatedField(
        many=True,
        slug_field="slug",
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = PublicProfileSerializer.Meta.fields + (
            "favorite_posts",
            "created_at",
            "updated_at",
        )

    def update(
        self,
        instance: Profile,
        validated_data,
    ):
        instance.bio = validated_data.get(
            "bio",
            instance.bio,
        )
        instance.full_name = validated_data.get(
            "full_name",
            instance.full_name,
        )

        profile_pic = validated_data.pop("profile_pic", None)
        if profile_pic is not None:
            instance.profile_pic = profile_pic

        instance.save()
        return instance
