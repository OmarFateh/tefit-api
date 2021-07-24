from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (CategorySerializer, CategoryListSerializer, PostListSerializer,
                          PostCreateSerializer, PostDetailSerializer)


##
# Category
##
class CategoryListAPIView(generics.ListAPIView):
    """
    Display a list of categories.
    """
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class CategoryPostListAPIView(generics.ListAPIView):
    """
    Display a list of posts of a category.
    """
    serializer_class = PostListSerializer

    def get_queryset(self, *args, **kwargs):
        # get category id from the requested url.
        category_slug = self.kwargs.get("slug", None)
        # get category all posts queryset.
        return Post.objects.filter(category__slug=category_slug)


class CategoryCreateAPIView(generics.CreateAPIView):
    """
    Category create API view.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Category detail update delete API view. 
    Only the admin can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self, *args, **kwargs):
        # get category slug from the requested url.
        category_slug = self.kwargs.get("slug", None)
        # get the category object by slug.
        obj = get_object_or_404(Category, slug=category_slug)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj


##
# Post
##
class PostsListAPIView(generics.ListAPIView):
    """
    Display a list of posts.
    """
    serializer_class = PostListSerializer
    queryset = Post.objects.select_related('category')


class PostCreateAPIView(generics.CreateAPIView):
    """
    Post create API view.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.select_related('category')
    serializer_class = PostCreateSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def perform_create(self, serializer):
        """
        Override the perform create function and let the post owner be the requested user.
        """
        serializer.save(author=self.request.user)


class PostDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Post detail update delete API view. 
    Only the owner of the post can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = Post.objects.select_related('category')
    serializer_class = PostDetailSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def get_object(self, *args, **kwargs):
        # get post slug from the requested url.
        post_slug = self.kwargs.get("slug", None)
        # get the post object by slug.
        obj = get_object_or_404(Post, slug=post_slug)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Update object's views count.
        """
        obj = self.get_object()
        obj.views_count = F('views_count') + 1
        obj.save()
        return self.retrieve(request, *args, **kwargs)
