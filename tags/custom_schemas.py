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
from .serializers import TagSerializer
from auth.custom_schemas import invalid_token_response
from typing import Mapping

tags_retrieve_schema = extend_schema(
    summary="Retrieve a tag",
    description="Retrieve a tag by its slug.",
    responses=TagSerializer(),
    tags=["Tag"],
)
tags_list_schema = extend_schema(exclude=True)

tags_schema: Mapping = {
    "retrieve": tags_retrieve_schema,
    "list": tags_list_schema,
}
