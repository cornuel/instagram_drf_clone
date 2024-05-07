from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from users import views as users_views
from profiles import views as profiles_views
from posts import views as posts_views
from tags import views as tags_views
from comments import views as comments_views
import feed.urls as feed
import search.urls as search
from decouple import config
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from app.schema import SpectacularElementsView, SpectacularRapiDocView

router = routers.DefaultRouter()
router.register(r'users',
                users_views.UsersViewSet,
                basename='users')
router.register(r'profiles',
                profiles_views.ProfileModelViewSet,
                basename='profiles')
router.register(r'posts',
                posts_views.PostViewSet,
                basename='posts')
router.register(r'tags',
                tags_views.TagViewSet,
                basename='tags')
router.register(r'comments',
                comments_views.CommentViewSet,
                basename='comments')
# router.register(r'feed',
#                 FeedView,
#                 basename='feed')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('api/feed/', include(feed)),
    path('api/search/', include(search)),
    path('api/token/', include('auth.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/elements/', SpectacularElementsView.as_view(url_name='schema'), name='elements'),
    path('api/schema/rapidoc/', SpectacularRapiDocView.as_view(url_name='schema'), name='rapidoc'),
]

if config("ENVIRONMENT") == 'dev':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)