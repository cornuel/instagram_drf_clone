from django.urls import path, include
from rest_framework import routers
from .views import ProfileModelViewSet

router = routers.DefaultRouter()
router.register(r'', ProfileModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]