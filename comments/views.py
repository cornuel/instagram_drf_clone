from django.shortcuts import render
from rest_framework import viewsets

from profiles.serializers import PublicProfileSerializer
from .serializers import CommentSerializer
from .models import Comment
from profiles.models import Profile
from app.permissions import IsAccountOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rich import print as rprint

# Create your views here.


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'

    permission_classes = {
        'list': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'retrieve': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'create': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'update': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to update this comment."
        },
        'partial_update': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to partially update this comment."
        },
        'destroy': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to delete this comment."
        },
        'like': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'likes': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
    }

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        action = self.action
        permissions = self.permission_classes.get(
            action, {}).get('classes', [])
        return [permission() for permission in permissions]

    def permission_denied(self, request, message=None, code=None):
        action = self.action  # Get the current action name
        error_message = self.permission_classes.get(
            action, {}).get('error_message', 'Permission denied.')
        raise PermissionDenied(error_message)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action == 'likes':
            return PublicProfileSerializer
        else:
            return CommentSerializer

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, post_id=None):
        queryset = self.queryset.filter(post__id=post_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        # Don't allow updating the post and parent field
        data = request.data.copy()
        data.pop('post', None)
        data.pop('parent', None)

        serializer = self.get_serializer(instance,
                                         data=data,
                                         partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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

    @action(detail=True, methods=['post'])
    def like(self, request, id: int = None):
        comment: Comment = self.get_object()
        profile: Profile = request.user.profile
        liked: bool = comment.likes.filter(user=request.user).exists()

        if liked:
            comment.likes.remove(profile)
            message = 'Comment unliked successfully'
        else:
            comment.likes.add(profile)
            message = 'Comment liked successfully'

        comment.save()
        serializer = self.get_serializer(comment)

        return Response({
            'message': message,
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })
        
    @action(detail=True, methods=['get'])
    def likes(self, request, id: int = None):
        comment: Comment = self.get_object()
        likes = comment.likes.all()
        serializer = self.get_serializer(likes, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
