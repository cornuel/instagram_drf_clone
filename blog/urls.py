"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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