# Generated by Django 4.2.5 on 2023-11-23 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]