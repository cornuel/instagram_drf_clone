import os
import tempfile
import zipfile

from django.shortcuts import get_object_or_404
import requests
from django.http import FileResponse
from django.db.models import Q, Count
from rest_framework import viewsets
from .serializers import PostDetailSerializer, PersonalPostListSerializer, PersonalPostDetailSerializer, PostsListSerializer
from .models import Post
from profiles.models import Profile
from tags.models import Tag
from tags.serializers import TagSerializer
from profiles.serializers import PublicProfileSerializer
from comments.serializers import CommentSerializer
from app.permissions import IsAccountOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from typing import List
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rich import print as rprint


class PostViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    serializer_class = PostsListSerializer
    queryset = Post.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    
    permission_classes = {
        'list': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'create': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'update': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to update this post."
        },
        'partial_update': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to partially update this post."
        },
        'destroy': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to delete this post."
        },
        'feature': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to feature this post."
        },
        'favorite': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        },
        'reset_upvote_count': {
            'classes': [IsAdminUser],
            'error_message': "You are not allowed."
        },
        'delete_all_posts': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to delete all posts."
        },
        'publish': {
            'classes': [IsAccountOwnerOrAdmin],
            'error_message': "You are not allowed to publish this post."
        },
        'favorited': {
            'classes': [IsAuthenticated],
            'error_message': "You are not authenticated."
        }
    }

    def permission_denied(self, request, message=None, code=None):
        action = self.action  # Get the current action name
        error_message = self.permission_classes.get(
            action, {}).get('error_message', 'Permission denied.')
        raise PermissionDenied(error_message)
    
    # def get_object(self):
    #     """
    #     Returns the object based on the current action.

    #     :param self: The instance of the class.
    #     :return: The object based on the current action.
    #     """
    #     if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
    #         assert self.lookup_field in self.kwargs
    #     return super().get_object()
            

    def get_serializer_class(self, *args, **kwargs):
        """
        Returns the serializer class based on the current action.

        :param self: The instance of the class.
        :return: The serializer class based on the current action.
        """
        # # This is a workaround to provide a serializer to the schema generator
        # # without needing a request or action.
        # if 'swagger_fake_view' in kwargs:
        #     return PersonalPostDetailSerializer(*args, **kwargs)
    
        if self.action:
            if self.action in ['list', 'favorited']:
                return PersonalPostListSerializer
            if self.action in ['create', 'publish']:
                return PersonalPostDetailSerializer
            if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'feature', 'like']:
                # Check if the authenticated user is the owner of the post
                if self.get_object().profile.user == self.request.user:
                    return PersonalPostDetailSerializer
                else:
                    return PostDetailSerializer
            if self.action == 'tags':
                return TagSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        # Filter the queryset to only include posts by the requesting profile
        if self.request and self.request.user.is_authenticated and self.action:
            if self.action == 'list':
                queryset = queryset.filter(profile=self.request.user.profile)
            elif self.action == 'retrieve':
                queryset = queryset.filter(
                    Q(is_private=False) | Q(profile=self.request.user.profile))
        return queryset
    
    # def get_object(self):
    #     """
    #     Returns the object the view is displaying.        
    #     """
    #     queryset = self.filter_queryset(self.get_queryset())

    #     # Perform the lookup filtering.
    #     lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

    #     filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    #     obj = get_object_or_404(queryset, **filter_kwargs)

    #     # May raise a permission denied
    #     self.check_object_permissions(self.request, obj)

    #     return obj

    def get_permissions(self):
        """
        Returns the list of permission instances that the current user has for the given action.

        :return: A list of permission instances.
        :rtype: list 
        """
        permissions = self.permission_classes.get(
            self.action, {}).get('classes', [])
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        profile = self.request.user.profile
        serializer.save(profile=profile)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='slug',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Slug of the post',
                required=True,
            )
        ],
        responses=PostDetailSerializer(many=False),
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='slug',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Slug of the post',
                required=True,
            )
        ],
        responses=PostDetailSerializer(many=False),
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves an instance of the object.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            Exception: If an error occurs while retrieving the object.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='slug',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Slug of the post',
                required=True,
            )
        ],
        responses=PostDetailSerializer(many=False),
    )
    def destroy(self, request, *args, **kwargs):
        """
        Deletes an instance of the object.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            Exception: If an error occurs while deleting the object.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.delete(instance)
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response("An error occurred while deleting the object.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='slug',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Slug of the post',
                required=True,
            )
        ],
        responses=PostDetailSerializer(many=False),
    )
    def update(self, request, *args, **kwargs):
        """
        Update the object with the given request data.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The updated serialized data of the object.
        """
        # Retrieve the post instance
        instance = self.get_object()

        # Update the fields specified in the request data
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='slug',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Slug of the post',
                required=True,
            )
        ],
        responses=PostDetailSerializer(many=False),
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update the object with the given request data.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The updated serialized data of the object.
        """
        # Retrieve the post instance
        instance = self.get_object()

        # Update the fields specified in the request data
        serializer = self.get_serializer(instance,
                                         data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def favorited(self, request):
        queryset = self.get_queryset().filter(is_private=False).filter(
            favorited_by__id=request.user.profile.id)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
    
    
    @action(detail=False, methods=['delete'])
    def delete_all_posts(self, request):
        # Delete all the posts of the requesting user
        self.get_queryset().delete()
        return Response({
            'message': 'Posts deleted.',
            'status': status.HTTP_204_NO_CONTENT,
        })

    @action(detail=True, methods=['get'])
    def tags(self, request, slug: str = None) -> Response:
        """
        Get the tags associated with a post.

        Parameters:
            request (Request): The request object.
            slug (str, optional): The slug of the post. Defaults to None.
        Returns:
            Response: The response object containing the serialized data of the tags.
        """
        post: Post = self.get_object()
        tags: List[Tag] = post.tags.all()
        serializer = self.get_serializer(tags, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @action(detail=True, methods=['post'])
    def feature(self, request, slug: str = None):
        """
        Feature or unfeature a post based on the given slug.
        Parameters:
            request (Request): The request object.
            slug (str, optional): The slug of the post. Defaults to None.
        Returns:
            Response: The response object containing the status and message.
        """
        post: Post = self.get_object()
        user_profile: Profile = post.profile

        if user_profile != request.user.profile:
            return Response({
                'message': 'You are not allowed to feature this post.',
                'status': status.HTTP_403_FORBIDDEN
            })

        if post.is_featured:
            post.is_featured = False
            post.save()
            serializer = self.get_serializer(post)
            return Response({
                'message': 'Post unfeatured successfully.',
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })

        # Check if the user has more than 3 featured posts
        featured_posts_count: int = Post.objects.filter(
            profile=user_profile, is_featured=True).count()
        if featured_posts_count >= 3:
            return Response({
                'message': 'Maximum limit of featured posts reached',
                'status': status.HTTP_400_BAD_REQUEST
            })

        post.is_featured = True
        post.save()
        serializer = self.get_serializer(post)
        return Response({
            'message': 'Post featured successfully',
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def favorite(self, request, slug: str = None):
        post: Post = self.get_object()
        profile = Profile.objects.prefetch_related(
            'favorite_posts').get(user=request.user)

        if post in profile.favorite_posts.all():
            profile.favorite_posts.remove(post)
            message = 'Post removed from favorites successfully'
        else:
            profile.favorite_posts.add(post)
            message = 'Post added to favorites successfully'

        profile.save()
        return Response({
            'message': message,
            'status': status.HTTP_200_OK
        })

    @action(detail=True, methods=['post'])
    def like(self, request, slug: str = None):
        post: Post = self.get_object()
        profile: Profile = request.user.profile
        liked: bool = post.likes.filter(user=request.user).exists()

        if liked:
            post.likes.remove(profile)
            message = 'Post unliked successfully'
        else:
            post.likes.add(profile)
            message = 'Post liked successfully'

        post.save()
        serializer = self.get_serializer(post)

        return Response({
            'message': message,
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })
        
    @action(detail=True, methods=['get'], serializer_class=PublicProfileSerializer)
    def likes(self, request, slug: str = None):
        post: Post = self.get_object()
        likes = post.likes.all()
        serializer = self.get_serializer(likes, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @action(detail=True, methods=['post'])
    def publish(self, request, slug: str = None):
        post: Post = self.get_object()

        if post.is_private:
            post.is_private = False
            message = 'Post published successfully'
        else:
            post.is_private = True
            message = 'Post unpublished successfully'
        post.save()
        serializer = self.get_serializer(post)
        return Response({
            'message': message,
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })
        
    @action(detail=True, methods=['get'])
    def download(self, request, slug: str = None):
        post: Post = self.get_object()
        # if post.images.count() == 1:
        #     ## problem -- the request takes forever then the image is corrupted, but the lengh is good
        #     image = post.images.first()
        #     image_url = image.image.url
        #     response = requests.get(image_url)
        #     response = FileResponse(w
        #         response.content,
        #         as_attachment=True)
        #     response['Content-Type'] = 'image/png'
        #     response['Content-Disposition'] = f'attachment; filename="{post.slug}.{image.image.name.split(".")[-1]}"'
        #     return response
        # else:
        zip_filename = f'{post.slug}.zip'
        zip_file = tempfile.NamedTemporaryFile(prefix=zip_filename, suffix='.zip', delete=False)
        try:
            with zipfile.ZipFile(zip_file.name, 'w') as zip_file_contents:
                for i, image in enumerate(post.images.all(), start=1):
                    image_filename = f'{post.slug}-{i}.{image.image.name.split(".")[-1]}'
                    image_url = image.image.url
                    response = requests.get(image_url)
                    zip_file_contents.writestr(image_filename, response.content)
                    
            zip_file.seek(0)
            response = FileResponse(zip_file)
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            
            return response
        except Exception as e:
            return Response("An error occurred while downloading the images.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        

    @action(detail=True, methods=['get'], serializer_class=CommentSerializer)
    def comments(self, request, slug: str = None):
        if self.request.method == 'GET':
            post: Post = self.get_object()
            comments = post.comments.filter(parent=None).annotate(like_count=Count('likes')).order_by('-like_count', '-created')
            serializer = self.get_serializer(comments, many=True)
            return self.get_paginated_response(self.paginate_queryset(serializer.data))

    @action(detail=True, methods=['get'], url_path='comment/(?P<comment_id>\d+)', serializer_class=CommentSerializer)
    def comment(self, request, slug=None, comment_id=None):
        post: Post = self.get_object()
        comment = post.comments.get(id=comment_id)
        subcomments = comment.replies.all()
        serializer = self.get_serializer(subcomments, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))
