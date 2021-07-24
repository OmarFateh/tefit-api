from django.shortcuts import get_object_or_404

from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Category, Post
from .mixins import PostReadTimeViewCountMixinSerializer, TimestampMixinSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.
    """
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        read_only_fields = ['id', 'slug']


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category list serializer.
    """
    published_posts_count = serializers.SerializerMethodField()
    all_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug',
                  'published_posts_count', 'all_posts_count']
        read_only_fields = ['id', 'slug']

    def get_published_posts_count(self, obj):
        return Post.objects.get_published_posts_list().filter(category_id=obj.id).count()

    def get_all_posts_count(self, obj):
        return Post.objects.filter(category_id=obj.id).count()


class PostListSerializer(serializers.ModelSerializer, TimestampMixinSerializer):
    """
    Post list serializer.
    """
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'overview', 'thumbnail', 'status', 'category',
                  'updated_at', 'created_at', 'timesince']


class PostCreateSerializer(serializers.ModelSerializer, PostReadTimeViewCountMixinSerializer, TimestampMixinSerializer):
    """
    Post create serializer.
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'overview', 'thumbnail', 'category', 'content', 'status',
                  'views_count', 'read_time', 'updated_at', 'created_at', 'timesince']

    def create(self, validated_data):
        """
        Create and return a new post.
        """
        request = self.context['request']
        category_id = request.data.get('category')
        if category_id is None or not isinstance(int(category_id), int):
            raise serializers.ValidationError(
                {'category': ['This field is invalid.']})
        category_instance = get_object_or_404(Category, id=category_id)
        return Post.objects.create(category=category_instance, **validated_data)


class PostDetailSerializer(serializers.ModelSerializer, PostReadTimeViewCountMixinSerializer, TimestampMixinSerializer):
    """
    Post detail serializer.
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'thumbnail', 'category', 'content', 'views_count', 'read_time',
                  'status', 'updated_at', 'created_at', 'timesince']
        read_only_fields = ['id', 'slug']

    def update(self, instance, validated_data):
        request = self.context['request']
        category_id = request.data.get('category')
        if category_id:
            if not isinstance(int(category_id), int):
                raise serializers.ValidationError(
                    {'category': ['This field is invalid.']})
            category_instance = get_object_or_404(Category, id=category_id)
            instance.category = category_instance
            instance.save()
        return super().update(instance, validated_data)
