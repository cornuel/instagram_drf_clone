from django.db import models
from django.contrib.auth.models import User
from django.db import models
from core.models import TimestampedModel
import os


def upload_to(instance, filename, suffix=""):
    return "{}/{}_pp{}".format(
        generate_subfolder(instance),
        instance.username,
        os.path.splitext(filename)[1],
    )


def generate_subfolder(instance):
    if hasattr(instance, "post"):
        profile = instance.post.profile
        username = profile.username
    else:
        username = instance.username
    return f"{username}"


class Profile(TimestampedModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    username = models.SlugField(
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(
        max_length=100,
        blank=True,
    )
    bio = models.TextField(
        max_length=300,
        blank=True,
    )
    profile_pic = models.ImageField(
        upload_to=upload_to,
        blank=True,
    )
    follows = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followed_by",
    )
    favorite_posts = models.ManyToManyField(
        "posts.Post",
        blank=True,
        related_name="favorited_by",
    )
    # saved_posts = models.ManyToManyField(
    #     'posts.Post', blank=True, related_name='saved_by')

    def __str__(self):
        return self.user.username
