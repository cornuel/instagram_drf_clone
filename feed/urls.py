from django.urls import path, include
from .views import FeedView

urlpatterns = [
    path('', FeedView.as_view()),
]
