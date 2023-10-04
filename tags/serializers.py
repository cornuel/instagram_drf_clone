from rest_framework import serializers
from django.utils.text import slugify
from django.db import IntegrityError
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'post_count')