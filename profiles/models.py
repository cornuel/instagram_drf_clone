from django.db import models
from django.contrib.auth.models import User
from django.db import models
from core.models import TimestampedModel
from app.utils import upload_to


class Profile(TimestampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    username = models.SlugField(max_length=255, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    profile_pic = models.ImageField(upload_to=upload_to)
    follows = models.ManyToManyField(
        'self', symmetrical=False, related_name='followed_by')
    favorite_posts = models.ManyToManyField(
        'posts.Post', blank=True, related_name='favorited_by')

    def __str__(self):
        return self.user.username
