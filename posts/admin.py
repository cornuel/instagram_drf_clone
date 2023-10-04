from django.contrib import admin
from .models import Post
# Register your models here.
admin.site.register(Post)

def delete_posts(modeladmin, request, queryset):
    queryset.delete()
    
# admin.site.add_action(delete_posts, "Delete selected posts")