from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
    PolymorphicProxySerializer,
)
from .serializers import CommentSerializer, RepliesSerializer
from profiles.serializers import ProfileListSerializer
from auth.custom_schemas import invalid_token_response
from typing import Mapping


comments_create_schema = extend_schema(
    summary="Create a comment",
    description="Create a comment.",
    responses=CommentSerializer(),
    tags=["Comment"],
)
comments_retrieve_schema = extend_schema(
    summary="Retrieve a comment",
    description="Retrieve a comment by its id.",
    responses=CommentSerializer(),
    tags=["Comment"],
)
comments_list_schema = extend_schema(exclude=True)
comments_update_schema = extend_schema(
    summary="Update a comment",
    description="Update a comment by its id. Can only be done by the owner of the comment.",
    responses=CommentSerializer(),
    tags=["Comment"],
)
comments_partial_update_schema = extend_schema(
    summary="Partially update a comment",
    description="Partially update a comment by its id. Can only be done by the owner of the comment.",
    responses=CommentSerializer(),
    tags=["Comment"],
)
comments_destroy_schema = extend_schema(
    summary="Delete a comment",
    description="Delete a comment by its id. Can only be done by the owner of the comment.",
    responses=CommentSerializer(),
    tags=["Comment"],
)
comments_like_schema = extend_schema(
    summary="Like a comment",
    description="Like a comment by its id.",
    responses=CommentSerializer(),
    tags=["Comment"],
)
comments_likes_schema = extend_schema(
    summary="Retrieve comment likes",
    description="Retrieve a list of Profiles that liked a comment by its id.",
    responses=CommentSerializer(),
    tags=["Comment"],
)

comments_schema: Mapping = {
    "create": comments_create_schema,
    "retrieve": comments_retrieve_schema,
    "list": comments_list_schema,
    "update": comments_update_schema,
    "partial_update": comments_partial_update_schema,
    "destroy": comments_destroy_schema,
    "like": comments_like_schema,
    "likes": comments_likes_schema,
}
