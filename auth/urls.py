from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView, MyTokenVerifyView

urlpatterns = [
    path('', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', MyTokenVerifyView.as_view(), name='token_verify'),
]