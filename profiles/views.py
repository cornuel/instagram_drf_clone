from django.shortcuts import render
from .serializers import ProfileDetailSerializer, ProfileListSerializer, PublicProfileSerializer
from .models import Profile
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


# Create your views here.
class ProfileModelViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    lookup_field = 'user__username'
    
    def get_serializer_class(self):
        """
        Returns the serializer class based on the current action.

        :param self: The instance of the class.
        :return: The serializer class based on the current action.
        """
        user = self.request.user
        # Check if the authenticated user is the owner of the profile, if so, return ProfileDetailSerializer
        if self.action == 'retrieve' and user == self.get_object().user:
            return ProfileDetailSerializer
        
        if self.action == 'list':
            return PublicProfileSerializer
        if self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return PublicProfileSerializer
        return super().get_serializer_class()
    
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        # Check if the authenticated user is the owner of the profile
        if instance.user != request.user:
            raise PermissionDenied("You are not allowed to edit this profile.")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)