from typing import List
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from posts.models import Post
from profiles.models import Profile
from posts.serializers import PostsListSerializer
from profiles.serializers import PublicProfileSerializer
from rest_framework.permissions import IsAuthenticated


class SearchView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        search_query = self.request.query_params.get('query', '')
        search_type = self.request.query_params.get(
            'type', '')  # type can be 'post' or 'profile'

        context = {'request': request}

        if search_type == 'post':
            # Query for matching posts
            posts = Post.objects.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(tags__name__icontains=search_query),
                is_private=False
            ).distinct().order_by('-created')

            # Paginate and serialize the posts
            paginated_posts = self.paginate_queryset(posts)
            post_serializer = PostsListSerializer(
                paginated_posts, many=True, context=context)

            return self.get_paginated_response({
                'posts': post_serializer.data,
            })

        elif search_type == 'tag':
            # Query for matching posts
            posts = Post.objects.filter(
                Q(tags__name__iexact=search_query),
                is_private=False
            ).distinct().order_by('-created')

            # Paginate and serialize the posts
            paginated_posts = self.paginate_queryset(posts)
            post_serializer = PostsListSerializer(
                paginated_posts, many=True, context=context)

            return self.get_paginated_response({
                'posts': post_serializer.data,
            })

        elif search_type == 'profile':
            # Query for matching profiles
            profiles = Profile.objects.filter(username__icontains=search_query)

            # Paginate and serialize the profiles
            paginated_profiles = self.paginate_queryset(profiles)
            profile_serializer = PublicProfileSerializer(
                paginated_profiles, many=True, context=context)

            return self.get_paginated_response({
                'profiles': profile_serializer.data,
            })

        else:
            # If no type or an invalid type was provided, return both posts and profiles
            posts = Post.objects.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(tags__name__icontains=search_query),
                is_private=False
            ).distinct().order_by('-created')

            profiles = Profile.objects.filter(username__icontains=search_query)

            paginated_posts = self.paginate_queryset(posts)
            paginated_profiles = self.paginate_queryset(profiles)

            post_serializer = PostsListSerializer(
                paginated_posts, many=True, context=context)
            profile_serializer = PublicProfileSerializer(
                paginated_profiles, many=True, context=context)

            return self.get_paginated_response({
                'profiles': profile_serializer.data,
                'posts': post_serializer.data,
            })
