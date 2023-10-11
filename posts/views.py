from django.shortcuts import render
from django.db import IntegrityError
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from .serializers import PostsListSerializer, CommentSerializer, PostDetailSerializer
from .models import Post, Comment
from tags.models import Tag
from blog.permissions import IsAccountOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    lookup_field = 'slug'
    
    permission_classes = {
        'create': [IsAuthenticated],
        'update': [IsAccountOwnerOrAdmin],
        'partial_update': [IsAccountOwnerOrAdmin],
        'destroy': [IsAccountOwnerOrAdmin],
        'toggle_feature': [IsAccountOwnerOrAdmin]
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
        if self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return PostDetailSerializer
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
    
@action(detail=True, methods=['post'])
def toggle_feature(self, request, slug=None):
    post: Post = self.get_object()
    user_profile = post.profile
    
    if post.is_featured:
        post.is_featured = False
        post.save()
        return Response({'message': 'Post unfeatured successfully'})
    
    # Check if the user has more than 3 featured posts
    featured_posts_count = Post.objects.filter(profile=user_profile, is_featured=True).count()
    if featured_posts_count >= 3:
        return Response({'message': 'Maximum limit of featured posts reached'}, status=status.HTTP_400_BAD_REQUEST)
    
    post.is_featured = True
    post.save()
    return Response({'message': 'Post featured successfully'})
    

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