# Generated by Django 4.2.5 on 2023-11-15 13:00

import profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_rename_image_profile_profile_pic_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic_url',
            field=models.ImageField(upload_to=profiles.models.upload_to),
        ),
    ]
