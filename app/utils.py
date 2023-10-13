from typing import List

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer

def paginate_objects(objects: List, request, serializer: Serializer, page_size: int) -> Response:
    """
    Paginates a list of objects based on the requested page number and page size.

    Parameters:
        objects (List): The list of objects to be paginated.
        request: The request object containing the query parameters.
        serializer: The serializer class for serializing the objects.
        page_size (int): The number of profiles to be displayed per page.

    Returns:
        Response: The paginated response containing the serialized objects.

    """
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_objects = paginator.paginate_queryset(objects, request)
    serialized_objects = serializer(paginated_objects, many=True)
    return paginator.get_paginated_response(serialized_objects.data)