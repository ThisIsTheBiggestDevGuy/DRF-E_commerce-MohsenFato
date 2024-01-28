from django.urls import path
from .views import (LoginView, RegisterUserView,
                    SellerProfileDetailView, SellerReviewCreateView, CreateSellerProfileView)

urlpatterns = [
    path('api-token-auth/', LoginView.as_view(), name='api_toke_auth'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('seller-profile/<int:pk>/', SellerProfileDetailView.as_view(), name='seller-profile-detail'),
    path('seller-reviews/',SellerReviewCreateView.as_view(),name='seller-review-create'),
    path('create-seller-profile/', CreateSellerProfileView.as_view(), name="create-seller-profile")
]
