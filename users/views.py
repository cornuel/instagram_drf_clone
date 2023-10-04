from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from blog.permissions import IsAccountOwnerOrAdmin
from rest_framework import status

class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    permission_classes = {
        'list': [IsAdminUser],
        'destroy': [IsAccountOwnerOrAdmin],
    }
    
    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list
        """
        permissions = self.permission_classes.get(self.action, [])
        return [permission() for permission in permissions]