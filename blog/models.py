from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django_resized import ResizedImageField
from ckeditor.fields import RichTextField


def post_image(instance, filename):
    """
    Upload the post image into the path and return the uploaded image path.
    """
    return f'posts/{instance.title}/{filename}'


class BaseTimestamp(models.Model):
    """
    Timestamp abstract model.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseTimestamp):
    """
    Category model.
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']

    def __str__(self):
        # Return category's title.
        return f"{self.title}"


class PostManager(models.Manager):
    """
    Override the post manager.
    """

    def get_published_posts_list(self):
        """
        Return a list of published posts.
        """
        return self.get_queryset().filter(status='published')


class Post(BaseTimestamp):
    """
    Post model.
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    # author = models.ForeignKey(
    #     User, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=post_image)
    # thumbnail = ResizedImageField(size=[750, 530], upload_to=post_image)
    content = RichTextField()
    views_count = models.IntegerField(default=0)
    read_time = models.PositiveIntegerField(default=1)
    published = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='published')

    objects = PostManager()

    class Meta:
        ordering = ['-published']

    def __str__(self):
        # Return post id and title.
        return f"{self.title}"
