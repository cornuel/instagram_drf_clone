from typing import List
from rest_framework import generics
from posts.models import Post
from profiles.models import Profile
from posts.serializers import PostsListSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Retrieve feed",
    description="Retrieve a paginated list of posts from followed profiles order by created date.",
    responses=PostsListSerializer(many=True),
    tags=["Feed"],
)
class FeedView(generics.ListAPIView):
    serializer_class = PostsListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve the user's profile
        user_profile: Profile = self.request.user.profile

        # Retrieve the profiles that the user follows
        followed_profiles: List[Profile] = user_profile.follows.all()

        # Retrieve all the posts from the followed profiles
        posts: List[Post] = Post.objects.filter(
            profile__in=followed_profiles,
            is_private=False,
        ).order_by("-created")

        return posts
