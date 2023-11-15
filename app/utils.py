import uuid
import os


def upload_to(instance, filename):
    # Generate a UUID for the filename
    uuid_filename = f"{uuid.uuid4().hex}{uuid.uuid4().hex}{uuid.uuid4().hex}"
    # Get the profile user's username
    if hasattr(instance, 'profile'):
        profile = instance.profile
    else:
        profile = instance
    username = profile.pk
    # Get the original file extension
    extension = os.path.splitext(filename)[1]
    # Construct the subfolder path
    subfolder = f"{username}"
    # Return the full path for the uploaded image
    return f"{subfolder}/{uuid_filename}{extension}"
