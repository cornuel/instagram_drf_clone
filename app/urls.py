from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users import views as users_views
from profiles import views as profiles_views
from posts import views as posts_views
from tags import views as tags_views

router = routers.DefaultRouter()
router.register(r'users', users_views.UsersViewSet,  basename='users')
router.register(r'profiles', profiles_views.ProfileModelViewSet,  basename='profiles')
router.register(r'posts', posts_views.PostViewSet,  basename='posts')
router.register(r'tags', tags_views.TagViewSet,  basename='tags')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', include('auth.urls')),
]