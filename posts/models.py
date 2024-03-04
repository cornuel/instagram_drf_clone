from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django_advance_thumbnail import AdvanceThumbnailField
import uuid
import os

def upload_to(instance, filename, suffix=""):
    uuid_filename = f"{instance.uuid.hex}"
    return f"{generate_subfolder(instance)}/{uuid_filename}{suffix}{os.path.splitext(filename)[1]}"

def generate_subfolder(instance):
    if hasattr(instance, 'post'):
        profile = instance.post.profile
        username = profile.username
    else:
        username = instance.username
    return f"{username}"

def upload_to_thumbnail(instance, filename):
    return upload_to(instance, filename, "_thumbnail")

class PostImage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)
    thumbnail = AdvanceThumbnailField(
        source_field='image', 
        upload_to=upload_to_thumbnail,
        null=True, 
        blank=True, 
        size=(512, 512)
    )

class Post(models.Model):
    profile = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        'profiles.Profile', blank=True, related_name='post_likes')
    view_count = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_featured = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    # slugify

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    for post_image in instance.images.all():
        post_image.image.delete(save=False)
        post_image.thumbnail.delete(save=False)