from django.urls import path

from .views import (CategoryListAPIView, CategoryPostListAPIView, CategoryCreateAPIView, CategoryUpdateDeleteAPIView,
                    PostsListAPIView, PostCreateAPIView, PostDetailUpdateDeleteAPIView)

"""
CLIENT
BASE ENDPOINT /api/blog/
"""

urlpatterns = [
    # category
    path('categories/list/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateAPIView.as_view(),
         name='category-create'),
    path('categories/<str:slug>/', CategoryUpdateDeleteAPIView.as_view(),
         name='category-detail'),
    path('categories/<str:slug>/posts/list/', CategoryPostListAPIView.as_view(),
         name='category-posts-list'),
    # post
    path('posts/list/', PostsListAPIView.as_view(), name='post-list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/<str:slug>/', PostDetailUpdateDeleteAPIView.as_view(),
         name='post-detail'),
]
