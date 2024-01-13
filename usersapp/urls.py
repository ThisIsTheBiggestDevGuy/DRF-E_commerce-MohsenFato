from django.urls import path
from .views import (LoginView, RegisterUserView)

urlpatterns = [
    path('api-token-auth/', LoginView.as_view(), name='api_toke_auth'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
]
