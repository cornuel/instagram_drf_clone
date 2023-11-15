from django.shortcuts import render
from rest_framework import viewsets
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
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsAccountOwnerOrAdmin],
        'partial_update': [IsAccountOwnerOrAdmin],
        'destroy': [IsAccountOwnerOrAdmin],
    }

    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list
        """
        permissions = self.permission_classes.get(self.action, [])
        return [permission() for permission in permissions]

    def permission_denied(self, request, message=None, code=None):
        action = self.action  # Get the current action name
        if action == 'destroy':
            error_message = "You are not allowed to delete this comment."
        elif action == 'update':
            error_message = "You are not allowed to update this comment."
        elif action == 'partial_update':
            error_message = "You are not allowed to update this comment."
        else:
            error_message = "Permission denied."

        raise PermissionDenied(error_message)

    def get_serializer_class(self):
        return super().get_serializer_class()

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

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
