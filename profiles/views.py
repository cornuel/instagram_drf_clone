from django.shortcuts import render
from .serializers import ProfileDetailSerializer, ProfileListSerializer, PublicProfileSerializer, SimpleProfileSerializer
from posts.serializers import PostsListSerializer
from .models import Profile
from django.contrib.auth.models import User
from posts.models import Post
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.permissions import IsAccountOwnerOrAdmin
from typing import List
    
class ProfileModelViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'user__username'
    
    permission_classes = {
        'list': [IsAdminUser],
        'retrieve': [IsAuthenticated],
        'update': [IsAccountOwnerOrAdmin],
        'partial_update': [IsAccountOwnerOrAdmin],
        'destroy': [IsAccountOwnerOrAdmin],
        'following': [IsAuthenticated],
        'followers': [IsAuthenticated],
        'posts': [IsAuthenticated],
    }
    
    def get_serializer_class(self):
        """
        Returns the serializer class based on the current action.

        :param self: The instance of the class.
        :return: The serializer class based on the current action.
        """
        user: User = self.request.user
        # Check if the authenticated user is the owner of the profile, if so, return ProfileDetailSerializer
        if self.action == 'retrieve':
            if self.get_object().user == user:
                return ProfileDetailSerializer
        
        if self.action == 'list':
            return ProfileListSerializer
        if self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy', 'following', 'followers']:
            return PublicProfileSerializer
        if self.action == 'posts':
            return PostsListSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list
        """
        permissions = self.permission_classes.get(self.action, [])
        return [permission() for permission in permissions]
    
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Update the profile of the authenticated user.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            Response: The updated serialized data of the profile.
        Raises:
            PermissionDenied: If the authenticated user is not the owner of the profile.
        """

        instance: Profile = self.get_object()
        # Check if the authenticated user is the owner of the profile
        if instance.user != request.user:
            raise PermissionDenied("You are not allowed to edit this profile.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts(self, request, user__username: str=None) -> Response:
        """
        Retrieves the posts associated with a user's profile.
        Parameters:
            request (Request): The incoming request object.
            user__username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The serialized data of the retrieved posts.
        """
        profile: Profile = self.get_object()
        posts: Post = profile.posts.all()
        serializer = self.get_serializer(posts, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
    
    @action(detail=True, methods=['post'])
    def follow(self, request, user__username: str = None) -> Response:
        """
        Follow or unfollow a user's profile.
        Parameters:
            request (Request): The HTTP request object.
            user__username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The HTTP response object containing a message indicating the result of the operation.
        """
        profile: Profile = self.get_object()
        
        if request.user.profile != profile:
            if request.user.profile.follows.filter(user__username=user__username).exists():
                request.user.profile.follows.remove(profile)
                message = f'You have unfollowed {profile.username}'
                _status = status.HTTP_200_OK
            else:
                request.user.profile.follows.add(profile)
                message = f'You are now following {profile.username}'
                _status = status.HTTP_200_OK
        else:
            message = 'You cannot follow yourself'
            _status = status.HTTP_400_BAD_REQUEST
        return Response({'message': message, 'status': _status})
    
    @action(detail=True, methods=['get'])
    def following(self, request, user__username: str = None) -> Response:
        """
        Retrieve the list of Profiles that the user is following
        Args:
            request (Request): The HTTP request object.
            user__username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The serialized data of the following.
        """
        
        profile: Profile = self.get_object()
        following: List[Profile] = profile.follows.all()
        serializer = self.get_serializer(following, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
    
    @action(detail=True, methods=['get'])
    def followers(self, request, user__username: str =None) -> Response:
        """
        Retrieve the list of Profiles following the user
        Args:
            request (Request): The request object.
            user__username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The serialized data of the followers.
        """
        profile: Profile = self.get_object()
        followers: List[Profile] = profile.followed_by.all()
        serializer = self.get_serializer(followers, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))