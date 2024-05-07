from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from app.throttles import BurstRateThrottle, SustainedRateThrottle
from .models import Tag
from .serializers import TagSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .custom_schemas import tags_schema
from drf_spectacular.utils import extend_schema_view


@extend_schema_view(**tags_schema)
class TagViewSet(viewsets.ModelViewSet):
    # only allow retrieve and list(if admin)
    http_method_names = ["get"]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    lookup_field = "slug"

    permission_classes = {
        "list": {
            "classes": [IsAdminUser],
            "error_message": "You are not allowed.",
        },
        "create": {
            "classes": [IsAuthenticated],
            "error_message": "You are not authenticated.",
        },
        "update": {
            "classes": [IsAdminUser],
            "error_message": "You are not allowed.",
        },
        "partial_update": {
            "classes": [IsAdminUser],
            "error_message": "You are not allowed.",
        },
        "destroy": {
            "classes": [IsAdminUser],
            "error_message": "You are not allowed.",
        },
    }

    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list
        """
        permissions = self.permission_classes.get(self.action, {}).get("classes", [])
        return [permission() for permission in permissions]

    def permission_denied(self, request, message=None, code=None):
        action = self.action  # Get the current action name
        error_message = self.permission_classes.get(action, {}).get(
            "error_message", "Permission denied."
        )
        raise PermissionDenied(error_message)

    def get_queryset(self):
        queryset = super().get_queryset().order_by("id")
        return queryset

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        slug = slugify(name)

        try:
            tag = Tag.objects.get(slug=slug)
            if tag:
                return Response(
                    "Tag with this name already exists.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Tag.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # @action(detail=False, methods=['delete'])
    # def delete_all(self, request):
    #     Tag.objects.all().delete()
    #     return Response("All tags have been deleted.", status=status.HTTP_204_NO_CONTENT)
