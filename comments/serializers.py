from rest_framework import serializers
from .models import Comment
from rich import print as rprint


class RepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'profile', 'post', 'body', 'created', 'parent')


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.StringRelatedField(read_only=True)
    like_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        many=False, view_name='comments-detail', lookup_field='id')

    def get_is_liked(self, obj: Comment) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.profile.id).exists()
        return False

    def get_like_count(self, obj: Comment) -> int:
        return obj.likes.count()
    
    def get_replies_count(self, obj: Comment) -> int:
        return obj.replies.count()

    class Meta:
        model = Comment
        fields = (
            'id', 
            'profile', 
            'post', 
            'body', 
            'parent', 
            'like_count', 
            'replies_count', 
            'is_liked', 
            'created', 
            'updated',
            'url'
        )
