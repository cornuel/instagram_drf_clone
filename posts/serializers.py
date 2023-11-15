from rest_framework import serializers
from .models import Post
from tags.models import Tag
from profiles.models import Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.text import slugify
from django.db.models import F
from profiles.serializers import PublicProfileSerializer


class TagListField(serializers.ListField):
    def to_internal_value(self, data):
        """
        Creating tags that don't already exist in the database and then returns the set of those tags.

        Parameters:
            data (Any): The external value to be converted.

        Returns:
            Set[Tag]: The set of internal tags corresponding to the external value.
        """
        # Create tags that do not exist
        tags = set()
        for tag_name in data:
            try:
                tag = Tag.objects.get(slug=slugify(tag_name))
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=tag_name.title())
            tags.add(tag)
        return tags

    def to_representation(self, data):
        return [self.child.to_representation(item) if item is not None else None for item in data.all()]


class PostsListSerializer(serializers.ModelSerializer):
    # profile = PublicProfileSerializer()
    profile = serializers.StringRelatedField(read_only=True)
    tags = TagListField(child=serializers.CharField(), required=False)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = (
            'id',
            'profile',
            'title',
            'image',
            'slug',
            'tags',
            'like_count',
            'comment_count'
        )


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagListField(child=serializers.CharField(), required=False)
    profile = serializers.StringRelatedField(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    def get_is_liked(self, obj: Post):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.profile.id).exists()
        return False

    def get_like_count(self, obj: Post):
        return obj.likes.count()

    def get_is_favorited(self, obj: Post):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.profile.id).exists()
        return False

    class Meta:
        model = Post
        fields = (
            'id',
            'profile',
            'title',
            'image',
            'body',
            'slug',
            'tags',
            'created',
            'updated',
            'is_liked',
            'is_favorited',
            'like_count',
            'view_count',
            'is_featured'
        )
        lookup_field = 'slug'

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])

        # Create brand new slug for the post
        slug = slugify(validated_data['title'])
        if slug and Post.objects.filter(slug=slug).exists():
            i = 1
            while Post.objects.filter(slug=f"{slug}-{i}").exists():
                i += 1
            validated_data['slug'] = f"{slug}-{i}"

        post = Post.objects.create(**validated_data)

        # Create tags that do not exist
        for tag in tags:
            post.tags.add(tag)
            # Increment the post_count for the related tag
            Tag.objects.filter(id=tag.id).update(
                post_count=F('post_count') + 1)
        post.save()

        return post

    def update(self, instance, validated_data):
        # Get the new set of tags
        new_tags = set(validated_data.pop('tags', []))

        # Get the old set of tags
        old_tags = set(instance.tags.all())

        # Find the tags that have been removed
        removed_tags = old_tags - new_tags

        # Find the tags that have been added
        added_tags = new_tags - old_tags

        # Decrement the post_count for each removed tag
        Tag.objects.filter(id__in=[tag.id for tag in removed_tags]).update(
            post_count=F('post_count') - 1
        )
        instance.tags.remove(*removed_tags)

        # Increment the post_count for each added tag
        Tag.objects.filter(id__in=[tag.id for tag in added_tags]).update(
            post_count=F('post_count') + 1
        )
        instance.tags.add(*added_tags)

        # Update the instance
        instance = super().update(instance, validated_data)

        # Add the new tags to the instance
        instance.tags.add(*new_tags)

        Tag.objects.filter(post_count=0).delete()

        return instance

    def delete(self, instance):
        # Get the tags associated with the instance
        tags = instance.tags.all()

        # Decrement the post_count for each tag
        Tag.objects.filter(id__in=tags).update(
            post_count=F('post_count') - 1
        )

        # Delete tags with post_count of 0
        Tag.objects.filter(post_count=0).delete()

        # Delete the instance
        instance.delete()
