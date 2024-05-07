from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from app.permissions import IsAccountOwnerOrAdmin
from rest_framework import status
from drf_spectacular.utils import extend_schema_view
from .custom_schemas import users_schema


@extend_schema_view(**users_schema)
class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    permission_classes = {
        "list": [IsAdminUser],
        "destroy": [IsAccountOwnerOrAdmin],
    }

    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list
        """
        permissions = self.permission_classes.get(self.action, [])
        return [permission() for permission in permissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def retrieve(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def update(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
