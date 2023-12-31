# Generated by Django 4.2.5 on 2023-10-12 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_rename_image_profile_profile_pic_url_and_more'),
        ('posts', '0006_remove_post_liked_by_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='profiles.profile'),
        ),
    ]
