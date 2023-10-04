from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Tag
from .serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
            
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        slug = slugify(name)
        print(slug)
        
        try:
            tag = Tag.objects.get(slug=slug)
            if tag:
                return Response("Tag with this name already exists.", status=status.HTTP_400_BAD_REQUEST)
        except Tag.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def list(self, request, *args, **kwargs):
        print('hi')
        return super().list(request, *args, **kwargs)