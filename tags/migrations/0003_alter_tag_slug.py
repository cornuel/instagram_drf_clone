# Generated by Django 4.2.5 on 2023-10-03 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
