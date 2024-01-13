from django.urls import path
from .views import (PostListCreateView, PostRetrieveUpdateDeleteView, CategoryListCreateView)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-retrieve-update-delete'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
]
