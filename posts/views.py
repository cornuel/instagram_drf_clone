from django.shortcuts import render
from django.db import IntegrityError
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from .serializers import PostsListSerializer, CommentSerializer, PostDetailSerializer
from .models import Post, Comment
from profiles.models import Profile
from tags.models import Tag
from tags.serializers import TagSerializer
from app.permissions import IsAccountOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from typing import List



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    lookup_field = 'slug'
    
    permission_classes = {
        'create': [IsAuthenticated],
        'update': [IsAccountOwnerOrAdmin],
        'partial_update': [IsAccountOwnerOrAdmin],
        'destroy': [IsAccountOwnerOrAdmin],
        'feature': [IsAccountOwnerOrAdmin],
        'favorite': [IsAuthenticated],
        'reset_upvote_count': [IsAdminUser],
    }
    
    def permission_denied(self, request, message=None, code=None):
        action = self.action  # Get the current action name
        if action == 'destroy':
            error_message = "You are not allowed to delete this post."
        elif action == 'update':
            error_message = "You are not allowed to update this post."
        elif action == 'partial_update':
            error_message = "You are not allowed to update this post."
        else:
            error_message = "Permission denied."

        raise PermissionDenied(error_message)

    
    def get_serializer_class(self):
        """
        Returns the serializer class based on the current action.

        :param self: The instance of the class.
        :return: The serializer class based on the current action.
        """
        if self.action == 'list':
            return PostsListSerializer
        if self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy', 'feature', 'like']:
            return PostDetailSerializer
        if self.action == 'tags':
            return TagSerializer
        return super().get_serializer_class()
    
    # def get_queryset(self):
    #     username = self.request.query_params.get('username')
        
    #     query = Post.objects.all()
        
    #     if username:
    #         return query.filter(user__username=username)

    #     return query
    
    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list
        """
        permissions = self.permission_classes.get(self.action, [])
        return [permission() for permission in permissions]
    
    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)
        
    def destroy(self, request, *args, **kwargs):
        """
        Deletes an instance of the object.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            Exception: If an error occurs while deleting the object.
        """

        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response("An error occurred while deleting the object.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        """
        Update the object with the given request data.

        Parameters:
            request (HttpRequest): The HTTP request object.
            args (list): Additional positional arguments.
            kwargs (dict): Additional keyword arguments.

        Returns:
            Response: The updated serialized data of the object.
        """
        # Retrieve the post instance
        instance = self.get_object()

        # Update the fields specified in the request data
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tags(self, request, slug: str=None) -> Response:
        """
        Get the tags associated with a post.
        
        Parameters:
            request (Request): The request object.
            slug (str, optional): The slug of the post. Defaults to None.
        Returns:
            Response: The response object containing the serialized data of the tags.
        """
        post: Post = self.get_object()
        tags: List[Tag] = post.tags.all()
        serializer = self.get_serializer(tags, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
    
    @action(detail=True, methods=['post'])
    def feature(self, request, slug: str=None):
        """
        Feature or unfeature a post based on the given slug.
        Parameters:
            request (Request): The request object.
            slug (str, optional): The slug of the post. Defaults to None.
        Returns:
            Response: The response object containing the status and message.
        """
        post: Post = self.get_object()
        user_profile: Profile = post.profile
        
        if user_profile != request.user.profile:
            return Response({
                'message': 'You are not allowed to feature this post.', 
                'status': status.HTTP_403_FORBIDDEN
            })
        
        if post.is_featured:
            post.is_featured = False
            post.save()
            serializer = self.get_serializer(post)
            return Response({
                'message': 'Post unfeatured successfully.',
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        
        # Check if the user has more than 3 featured posts
        featured_posts_count: int = Post.objects.filter(profile=user_profile, is_featured=True).count()
        if featured_posts_count >= 3:
            return Response({
                'message': 'Maximum limit of featured posts reached', 
                'status': status.HTTP_400_BAD_REQUEST
            })
        
        post.is_featured = True
        post.save()
        serializer = self.get_serializer(post)
        return Response({
            'message': 'Post featured successfully',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def favorite(self, request, slug: str =None):
        post: Post = self.get_object()
        profile = Profile.objects.prefetch_related('favorite_posts').get(user=request.user)
        
        if post in profile.favorite_posts.all():
            profile.favorite_posts.remove(post)
            message = 'Post removed from favorites successfully'
        else:
            profile.favorite_posts.add(post)
            message = 'Post added to favorites successfully'
            
        profile.save()
        return Response({
            'message': message, 
            'status': status.HTTP_200_OK
        })
    
    @action(detail=True, methods=['post'])
    def like(self, request, slug: str =None):
        post: Post = self.get_object()
        profile: Profile = request.user.profile
        liked: bool = post.likes.filter(user=request.user).exists()

        if liked:
            post.likes.remove(profile)
            message = 'Post unliked successfully'
        else:
            post.likes.add(profile)
            message = 'Post liked successfully'
        
        post.save()
        serializer = self.get_serializer(post)
        
        return Response({
            'message': message, 
            'status': status.HTTP_200_OK,
            'data': serializer.data
            })
    
# class UserPostViewSet(viewsets.ReadOnlyModelViewSet):
#     lookup_field = 'user'

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return PostsListSerializer
#         if self.action == 'retrieve':
#             return PostDetailSerializer
#         return super().get_serializer_class()

#     def get_queryset(self):
#         username = self.kwargs.get('username')
#         print(username)
        
#         # Check if the user with the provided username exists
#         try:
#             user = User.objects.get(user__username=username)
#         except User.DoesNotExist:
#             raise NotFound(f"User with username '{username}' does not exist.")

#         # If the user exists, filter posts by that user
#         return Post.objects.filter(user=user)

    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()