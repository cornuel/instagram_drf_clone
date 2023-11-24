from typing import List
from rest_framework import generics
from posts.models import Post
from profiles.models import Profile
from posts.serializers import PostsListSerializer


class FeedView(generics.ListAPIView):
    serializer_class = PostsListSerializer

    def get_queryset(self):
        # Retrieve the user's profile
        user_profile: Profile = self.request.user.profile

        # Retrieve the profiles that the user follows
        followed_profiles: List[Profile] = user_profile.follows.all()

        # Retrieve all the posts from the followed profiles
        posts: List[Post] = Post.objects.filter(
            profile__in=followed_profiles, is_private=False).order_by('-created')

        return posts
