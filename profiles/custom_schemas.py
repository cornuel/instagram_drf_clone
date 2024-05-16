from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiExample,
    OpenApiResponse,
    PolymorphicProxySerializer,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from auth.custom_schemas import invalid_token_response
from .serializers import (
    ProfileDetailSerializer,
    ProfileListSerializer,
    PublicProfileSerializer,
)
from posts.serializers import PostsListSerializer
from typing import Mapping

profiles_retrieve_schema = extend_schema(
    summary="Retrieve a profile",
    description="Retrieve a profile by username.",
    tags=["Profile"],
    responses={
        200: OpenApiResponse(
            PolymorphicProxySerializer(
                component_name="MetaProfile",
                serializers={
                    "PublicProfile": PublicProfileSerializer,
                    "ProfileDetail": ProfileDetailSerializer,
                },
                resource_type_field_name="",
            )
        ),
        404: OpenApiResponse(
            description="No Profile matches the given query.",
            response=inline_serializer(
                name="404Follow",
                fields={"detail": serializers.CharField()},
            ),
            examples=[
                OpenApiExample(
                    name="Not Found",
                    media_type="application/json",
                    status_codes=[404],
                    value={"detail": "No Profile matches the given query."},
                ),
            ],
        ),
    },
)
profiles_list_schema = extend_schema(
    exclude=True,
)
profiles_create_schema = extend_schema(
    exclude=True,
)
profiles_destroy_schema = extend_schema(
    # summary="Delete your profile",
    # description="Can only be done by the owner of the profile.",
    # tags=["Profile"],
    # responses=None,
    exclude=True,
)
profiles_update_schema = extend_schema(
    summary="Update your profile",
    description="Can only be done by the owner of the profile.",
    tags=["Profile"],
    responses={
        200: ProfileDetailSerializer,
    },
)
profiles_delete_profile_pic_schema = extend_schema(
    summary="Delete your profile picture",
    description="Can only be done by the owner of the profile.",
    tags=["Profile"],
    responses={
        200: ProfileDetailSerializer,
    },
)
profiles_posts_schema = extend_schema(
    summary="Retrieve a user's posts",
    description="Retrieves the posts associated with a user's profile.",
    tags=["Post"],
    responses={
        200: PostsListSerializer(many=True),
    },
)
profiles_follow_schema = extend_schema(
    summary="Follow/unfollow a user's profile",
    description="Follow or unfollow a user's profile.",
    tags=["Follow"],
    request=None,
    responses={
        200: OpenApiResponse(
            description="The profile has been followed or unfollowed.",
            response=inline_serializer(
                name="Follow",
                fields={
                    "message": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Follow",
                    media_type="application/json",
                    status_codes=[200],
                    value={"message": "You are now following {username}."},
                ),
                OpenApiExample(
                    name="Unfollow",
                    media_type="application/json",
                    status_codes=[200],
                    value={"message": "You have successfully unfollowed {username}."},
                ),
            ],
        ),
        200: OpenApiResponse(
            description="The profile has been followed or unfollowed.",
            response=inline_serializer(
                name="Follow",
                fields={
                    "message": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Follow",
                    media_type="application/json",
                    status_codes=[200],
                    value={"message": "You are now following {username}."},
                ),
                OpenApiExample(
                    name="Unfollow",
                    media_type="application/json",
                    status_codes=[200],
                    value={"message": "You have successfully unfollowed {username}."},
                ),
            ],
        ),
        400: OpenApiResponse(
            description="You cannot follow yourself.",
            response=inline_serializer(
                name="Follow",
                fields={
                    "message": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Follow Self",
                    media_type="application/json",
                    status_codes=[400],
                    value={"message": "You cannot follow yourself"},
                ),
            ],
        ),
        401: OpenApiResponse(
            description="Invalid or expired token.",
            response=invalid_token_response,
            examples=[
                OpenApiExample(
                    name="Invalid Token",
                    media_type="application/json",
                    status_codes=[401],
                    value=invalid_token_response,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="No Profile matches the given query.",
            response=inline_serializer(
                name="404Follow",
                fields={
                    "detail": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Not Found",
                    media_type="application/json",
                    status_codes=[404],
                    value={"detail": "No Profile matches the given query."},
                ),
            ],
        ),
    },
)
profiles_following_schema = extend_schema(
    summary="Retrieve list of following",
    description="Retrieves the list of Profiles that a user is following.",
    tags=["Follow"],
    request=None,
    responses={
        200: PublicProfileSerializer(many=True),
        401: OpenApiResponse(
            description="Invalid or expired token.",
            response=invalid_token_response,
            examples=[
                OpenApiExample(
                    name="Invalid Token",
                    media_type="application/json",
                    status_codes=[401],
                    value=invalid_token_response,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="No Profile matches the given query.",
            response=inline_serializer(
                name="404Follow",
                fields={
                    "detail": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Not Found",
                    media_type="application/json",
                    status_codes=[404],
                    value={"detail": "No Profile matches the given query."},
                ),
            ],
        ),
    },
)
profiles_followers_schema = extend_schema(
    summary="Retrieve list of followers",
    description="Retrieves the list of Profiles that follows the user.",
    tags=["Follow"],
    request=None,
    responses={
        200: PublicProfileSerializer(many=True),
        401: OpenApiResponse(
            description="Invalid or expired token.",
            response=invalid_token_response,
            examples=[
                OpenApiExample(
                    name="Invalid Token",
                    media_type="application/json",
                    status_codes=[401],
                    value=invalid_token_response,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="No Profile matches the given query.",
            response=inline_serializer(
                name="404Follow",
                fields={
                    "detail": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Not Found",
                    media_type="application/json",
                    status_codes=[404],
                    value={"detail": "No Profile matches the given query."},
                ),
            ],
        ),
    },
)
profiles_isFollowing_schema = extend_schema(
    summary="Is auth user following profile",
    description="Check if the authenticated user is following the specified Profile.",
    tags=["Follow"],
    request=None,
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="200Follow",
                fields={
                    "is_following": serializers.BooleanField(
                        required=False,
                    )
                },
            )
        ),
        401: OpenApiResponse(
            description="Invalid or expired token.",
            response=invalid_token_response,
            examples=[
                OpenApiExample(
                    name="Invalid Token",
                    media_type="application/json",
                    status_codes=[401],
                    value=invalid_token_response,
                ),
            ],
        ),
        404: OpenApiResponse(
            description="No Profile matches the given query.",
            response=inline_serializer(
                name="404Follow",
                fields={
                    "detail": serializers.CharField(
                        required=False,
                    )
                },
            ),
            examples=[
                OpenApiExample(
                    name="Not Found",
                    media_type="application/json",
                    status_codes=[404],
                    value={"detail": "No Profile matches the given query."},
                ),
            ],
        ),
    },
)


profiles_schema: Mapping = {
    "retrieve": profiles_retrieve_schema,
    "list": profiles_list_schema,
    "create": profiles_create_schema,
    "destroy": profiles_destroy_schema,
    "update": profiles_update_schema,
    "delete_profile_pic": profiles_delete_profile_pic_schema,
    "posts": profiles_posts_schema,
    "follow": profiles_follow_schema,
    "following": profiles_following_schema,
    "followers": profiles_followers_schema,
    "isFollowing": profiles_isFollowing_schema,
}
