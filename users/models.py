from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        instance.profile = Profile.objects.create(
            user=instance, username=instance.username)
