from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
    PolymorphicProxySerializer,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers
from auth.custom_schemas import invalid_token_response
from .serializers import (
    PersonalPostDetailSerializer,
    PostDetailSerializer,
    PostsListSerializer,
)
from profiles.serializers import ProfileListSerializer
from comments.serializers import CommentSerializer
from typing import Mapping

posts_retrieve_schema = extend_schema(
    summary="Retrieve a post",
    description="Retrieve a post by its slug.",
    parameters=[
        OpenApiParameter(
            name="slug",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Slug of the post",
            required=True,
        )
    ],
    responses=PostDetailSerializer(many=False),
    tags=["Post"],
)
posts_list_schema = extend_schema(
    summary="Retrieve own posts",
    description="Retrieve a paginated list of posts created by the authenticated user.",
    tags=["Post"],
)
posts_create_schema = extend_schema(
    summary="Create a post",
    description="Create a post.",
    responses=PersonalPostDetailSerializer(many=False),
    tags=["Post"],
)
posts_destroy_schema = extend_schema(
    summary="Delete a post",
    description="Delete a post by its slug.",
    tags=["Post"],
    parameters=[
        OpenApiParameter(
            name="slug",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Slug of the post",
            required=True,
        )
    ],
    responses=PostDetailSerializer(many=False),
)
posts_update_schema = extend_schema(
    summary="Update a post",
    description="Update a post by its slug.",
    tags=["Post"],
    parameters=[
        OpenApiParameter(
            name="slug",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Slug of the post",
            required=True,
        )
    ],
    responses=PostDetailSerializer(many=False),
)
posts_partial_update_schema = extend_schema(
    summary="Partially update a post",
    description="Partially update a post by its slug.",
    tags=["Post"],
    parameters=[
        OpenApiParameter(
            name="slug",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Slug of the post",
            required=True,
        )
    ],
    responses=PostDetailSerializer(many=False),
)
posts_favorited_schema = extend_schema(
    summary="Retrieve saved posts",
    description="Retrieve your favorited posts.",
    responses=PostsListSerializer(many=True),
    tags=["Post"],
)
posts_favorite_schema = extend_schema(
    summary="Save/Unsave a post to favorite",
    description="Save or unsave a post to favorite by its slug.",
    responses=PostDetailSerializer(),
    tags=["Post"],
)
posts_delete_all_posts_schema = extend_schema(
    summary="Delete all posts",
    description="Delete all posts created by the authenticated user.",
    tags=["Post"],
)
posts_tags_schema = extend_schema(
    summary="Retrieve tags associated with post",
    description="Retrieve a list of tags associated with a post.",
    responses=PostsListSerializer(many=True),
    tags=["Tag"],
)
posts_feature_schema = extend_schema(
    summary="Feature/Unfeature a post",
    description="Feature or unfeature a post by its slug.",
    responses=PostDetailSerializer(),
    tags=["Post"],
)
posts_like_schema = extend_schema(
    summary="Like/Unlike a post",
    description="Like or unlike a post by its slug.",
    responses=PostDetailSerializer(),
    tags=["Post"],
)
posts_likes_schema = extend_schema(
    summary="Retrieve likes of a post",
    description="Retrieve the list of Profiles that has liked a post by its slug.",
    responses=ProfileListSerializer(many=True),
    tags=["Post"],
)
posts_publish_schema = extend_schema(
    summary="Publish/Unpublish a post",
    description="Publish or unpublish a post by its slug.",
    responses=PostDetailSerializer(),
    tags=["Post"],
)
posts_download_schema = extend_schema(
    summary="Download post images",
    description="Download all the post images in a zip file.",
    responses=PostDetailSerializer(),
    tags=["Post"],
)
posts_comments_schema = extend_schema(
    summary="Retrieve comments of a post",
    description="Retrieve the list of comments associated with a post by its slug. Comments are ordered by number of likes and creation date",
    responses=CommentSerializer(many=True),
    tags=["Comment"],
)
posts_comment_schema = extend_schema(
    summary="Retrieve replies of a comment",
    description="Retrieve the list of replies associated with a comment by its id. Replies are ordered by number of likes and creation date",
    responses=CommentSerializer(many=True),
    tags=["Comment"],
)

posts_schema: Mapping = {
    "retrieve": posts_retrieve_schema,
    "list": posts_list_schema,
    "create": posts_create_schema,
    "destroy": posts_destroy_schema,
    "update": posts_update_schema,
    "partial_update": posts_partial_update_schema,
    "favorited": posts_favorited_schema,
    "favorite": posts_favorite_schema,
    "delete_all_posts": posts_delete_all_posts_schema,
    "tags": posts_tags_schema,
    "feature": posts_feature_schema,
    "like": posts_like_schema,
    "likes": posts_likes_schema,
    "publish": posts_publish_schema,
    "download": posts_download_schema,
    "comments": posts_comments_schema,
    "comment": posts_comment_schema,
}
