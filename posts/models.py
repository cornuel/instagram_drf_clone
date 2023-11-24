from django.db import models
from django.contrib.auth.models import User
from tags.models import Tag
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_delete
from app.utils import upload_to


class Post(models.Model):
    profile = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to)
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


@receiver(post_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    instance.image.delete(False)
