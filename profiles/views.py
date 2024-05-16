from django.shortcuts import render

from app.throttles import BurstRateThrottle, SustainedRateThrottle
from .serializers import (
    ProfileDetailSerializer,
    ProfileListSerializer,
    PublicProfileSerializer,
    SimpleProfileSerializer,
    FollowResponseSerializer,
)
from posts.serializers import PostsListSerializer
from .models import Profile
from django.contrib.auth.models import User
from posts.models import Post
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.permissions import IsAccountOwnerOrAdmin
from typing import List
from drf_spectacular.utils import extend_schema_view
from auth.custom_schemas import invalid_token_response
from .custom_schemas import profiles_schema


@extend_schema_view(**profiles_schema)
class ProfileModelViewSet(viewsets.ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "delete",
        "head",
        "options",
        "put",
    ]
    queryset = Profile.objects.all()
    serializer_class = PublicProfileSerializer
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    lookup_field = "username"

    permission_classes = {
        "list": {
            "classes": [IsAdminUser],
            "error_message": "You are not allowed to list profiles.",
        },
        "retrieve": {
            "classes": [IsAuthenticated],
            "error_message": "You are not authenticated.",
        },
        "update": {
            "classes": [IsAccountOwnerOrAdmin],
            "error_message": "You are not allowed to update this profile.",
        },
        "partial_update": {
            "classes": [IsAccountOwnerOrAdmin],
            "error_message": "You are not allowed to partially update this profile.",
        },
        "destroy": {
            "classes": [IsAccountOwnerOrAdmin],
            "error_message": "You are not allowed to delete this profile.",
        },
        "isFollowing": {
            "classes": [IsAuthenticated],
            "error_message": "You are not authenticated.",
        },
        "following": {
            "classes": [IsAuthenticated],
            "error_message": "You are not authenticated.",
        },
        "followers": {
            "classes": [IsAuthenticated],
            "error_message": "You are not authenticated.",
        },
        "delete_profile_pic": {
            "classes": [IsAccountOwnerOrAdmin],
            "error_message": "You are not allowed to update this profile.",
        },
        "posts": {
            "classes": [IsAuthenticated],
            "error_message": "You are not authenticated.",
        },
    }

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        action = self.action
        permissions = self.permission_classes.get(action, {}).get("classes", [])
        return [permission() for permission in permissions]

    def permission_denied(self, request, message=None, code=None):
        action = self.action  # Get the current action name
        error_message = self.permission_classes.get(action, {}).get(
            "error_message", "Permission denied."
        )
        raise PermissionDenied(error_message)

    def get_serializer_class(self):
        """
        Returns the serializer class based on the current action.

        :param self: The instance of the class.
        :return: The serializer class based on the current action.
        """
        user: User = self.request.user
        # Check if the authenticated user is the owner of the profile, if so, return ProfileDetailSerializer
        if self.action in ["retrieve", "delete_profile_pic"]:
            if self.get_object().user == user:
                return ProfileDetailSerializer
            else:
                return PublicProfileSerializer
        elif self.action == "update":
            return ProfileDetailSerializer
        elif self.action == "list":
            return ProfileListSerializer
        elif self.action == "posts":
            return PostsListSerializer
        else:
            # 'create', 'retrieve', 'update', 'partial_update', 'destroy'
            # 'following', 'followers', 'isFollowing'
            return super().get_serializer_class()

    # VIEWS
    ########################################

    # The profile is automatically created on user creation
    def create(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

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

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ACTIONS
    ########################################

    @action(detail=True, methods=["delete"])
    def delete_profile_pic(self, request, username: str = None) -> Response:
        """g
        Delete the profile picture of the authenticated user.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            Response: The updated serialized data of the profile without the profile picture.
        Raises:
            PermissionDenied: If the authenticated user is not the owner of the profile.
        """
        profile: Profile = self.get_object()
        if profile.user != request.user:
            self.permission_denied(request)
        profile.profile_pic.delete()
        profile.save()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def posts(self, request, username: str = None):
        """
        Retrieves the posts associated with a user's profile.
        Parameters:
            request (Request): The incoming request object.
            username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The serialized data of the retrieved posts.
        """
        profile: Profile = self.get_object()
        posts: Post = profile.posts.filter(is_private=False).order_by("-created")
        serializer = self.get_serializer(
            posts,
            many=True,
        )
        results = self.get_paginated_response(self.paginate_queryset(serializer.data))
        return results

    @action(detail=True, methods=["post"])
    def follow(self, request, username: str = None) -> Response:
        """
        Follow or unfollow a user's profile.
        Parameters:
            request (Request): The HTTP request object.
            username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The HTTP response object containing a message indicating the result of the operation.
        """
        profile: Profile = self.get_object()

        if request.user.profile != profile:
            if request.user.profile.follows.filter(username=username).exists():
                request.user.profile.follows.remove(profile)
                message = f"You have successfully unfollowed {profile.username}"
                _status = status.HTTP_200_OK
            else:
                request.user.profile.follows.add(profile)
                message = f"You are now following {profile.username}"
                _status = status.HTTP_200_OK
        else:
            message = "You cannot follow yourself"
            _status = status.HTTP_400_BAD_REQUEST
        return Response(
            {
                "message": message,
                "status": _status,
            }
        )

    @action(detail=True, methods=["get"])
    def following(self, request, username: str = None) -> Response:
        """
        Retrieve the list of Profiles that the user is following
        Args:
            request (Request): The HTTP request object.
            username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The serialized data of the following.
        """

        profile: Profile = self.get_object()
        following: List[Profile] = profile.follows.all()
        serializer = self.get_serializer(
            following,
            many=True,
        )
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @action(detail=True, methods=["get"])
    def followers(self, request, username: str = None) -> Response:
        """
        Retrieve the list of Profiles following the user
        Args:
            request (Request): The request object.
            username (str, optional): The username of the user. Defaults to None.
        Returns:
            Response: The serialized data of the followers.
        """
        profile: Profile = self.get_object()
        followers: List[Profile] = profile.followed_by.all()
        serializer = self.get_serializer(
            followers,
            many=True,
        )
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @action(detail=True, methods=["get"])
    def isFollowing(self, request, username: str = None) -> Response:
        """
        Check if the authenticated user is following the specified profile.
        Args:
            request (Request): The HTTP request object.
            username (str, optional): The username of the profile. Defaults to None.
        Returns:
            Response: The serialized data indicating if the user is following the profile.
        """

        profile: Profile = self.get_object()
        user = request.user

        is_following = profile.followed_by.filter(id=user.id).exists()
        return Response(
            {
                "is_following": is_following,
            }
        )
