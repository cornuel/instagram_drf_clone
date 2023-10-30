from rest_framework import serializers
from .models import Comment
from rich import print as rprint

class RepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'profile', 'post', 'body', 'created', 'parent')

class CommentSerializer(serializers.ModelSerializer):
    # replies = RepliesSerializer(many=True)
    profile = serializers.StringRelatedField(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj: Comment):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.profile.id).exists()
        return False    

    def get_like_count(self, obj: Comment):
        return obj.likes.count()
    
    class Meta:
        model = Comment
        fields = ('id', 'profile', 'post', 'body', 'created', 'updated', 'parent', 'like_count', 'is_liked')
        
        