from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
    PolymorphicProxySerializer,
)
from typing import Mapping

users_create_schema = extend_schema(
    summary="Create a user",
    description="Create a user.",
    tags=["User"],
)
users_retrieve_schema = extend_schema(
    exclude=True,
)
users_list_schema = extend_schema(
    exclude=True,
)
users_destroy_schema = extend_schema(
    summary="Delete a user",
    description="Delete a user by its username. Can only be done by the owner of the user.",
    tags=["User"],
)
users_update_schema = extend_schema(
    exclude=True,
)
users_partial_update_schema = extend_schema(
    exclude=True,
)

users_schema: Mapping = {
    "create": users_create_schema,
    "retrieve": users_retrieve_schema,
    "list": users_list_schema,
    "destroy": users_destroy_schema,
    "update": users_update_schema,
    "partial_update": users_partial_update_schema,
}
