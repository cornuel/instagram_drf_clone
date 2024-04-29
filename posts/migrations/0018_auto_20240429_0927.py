from django.db import migrations

def fix_view_count(apps, schema_editor):
    Post = apps.get_model('posts', 'Post')
    for post in Post.objects.filter(view_count__isnull=True):
        post.view_count = 0
        post.save()
        
class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_alter_post_view_count'),
    ]

    operations = [
        migrations.RunPython(fix_view_count),
    ]