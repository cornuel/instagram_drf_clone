from django.urls import path, include
from .views import SearchView

urlpatterns = [
    path('', SearchView.as_view()),
]
