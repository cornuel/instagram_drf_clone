from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from tags.models import Tag
from django.utils.text import slugify

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='posts')
    title = models.CharField(max_length = 100)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    likes = models.ManyToManyField(Profile, blank=True, related_name='liked_by')
    view_count = models.IntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # slugify
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="replies",
    )

    def __str__(self):
        return self.name + " " + str(self.date)