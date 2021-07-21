from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Category, Post
from .mixins import PostReadTimeViewCountMixinSerializer, TimestampMixinSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer.
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
    author = UserSerializer(read_only=True)
    post_url = serializers.HyperlinkedIdentityField(
        view_name='blog-api:post-detail', lookup_field='slug')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'slug', 'overview', 'thumbnail', 'post_url', 'status', 'category',
                  'updated_at', 'created_at', 'timesince']


class PostCreateSerializer(serializers.ModelSerializer, PostReadTimeViewCountMixinSerializer, TimestampMixinSerializer):
    """
    Post create serializer.
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'title', 'overview', 'thumbnail', 'category', 'content', 'status',
                  'views_count', 'read_time', 'updated_at', 'created_at', 'timesince']

    # def create(self, validated_data):
    #     """
    #     Create and return a new post.
    #     """
    #     request = self.context['request']
    #     author = request.user
    #     thumbnail = validated_data['thumbnail']
    #     caption = validated_data.get('caption', None)
    #     hashtags = validated_data.get('hashtags', None)
    #     # create new item with the submitted data.
    #     new_item = Item.objects.create(
    #         owner=owner, image=image, caption=caption)
    #     # if the submitted data has hashtags.
    #     if hashtags:
    #         # convert the submitted hashtags string to a hashtags queryset.
    #         hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags)
    #         # add hashtags to the item's hashtags.
    #         new_item.hashtags.set(hashtags_qs)
    #     return new_item


class PostDetailSerializer(serializers.ModelSerializer, PostReadTimeViewCountMixinSerializer, TimestampMixinSerializer):
    """
    Post detail serializer.
    """
    author = UserSerializer(read_only=True)
    # title = serializers.CharField(max_length=180, allow_blank=True)
    # thumbnail = serializers.ImageField(allow_empty_file=True)
    # content = serializers.CharField(allow_blank=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'slug', 'thumbnail', 'category', 'content', 'views_count', 'read_time',
                  'status', 'updated_at', 'created_at', 'timesince']
        read_only_fields = ['id', 'author', 'slug']

    # def update(self, instance, validated_data):
    #     request = self.context['request']
    #     # hashtags = validated_data.get('update_hashtags', None)
    #     # update item
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.thumbnail = validated_data.get(
    #         'thumbnail', instance.thumbnail)
    #     instance.content = validated_data.get('content', instance.content)
    #     # if hashtags:
    #     #     # convert the submitted hashtags string to a hashtags queryset.
    #     #     hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags)
    #     #     # add hashtags to the item's hashtags.
    #     #     instance.hashtags.set(hashtags_qs)
    #     instance.save()
    #     return super().update(instance, validated_data)
