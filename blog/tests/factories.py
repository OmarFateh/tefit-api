import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

import factory

from blog.models import Category, Post
from accounts.tests.factories import UserFactory

upload_file = open(os.path.join(settings.BASE_DIR,
                                'static/img/no_avatar.jpg'), "rb")


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Create new category instance.
    """
    class Meta:
        model = Category
        django_get_or_create = ('slug',)

    title = 'fitness'
    slug = 'fitness'


class PostFactory(factory.django.DjangoModelFactory):
    """
    Create new post instance.
    """
    class Meta:
        model = Post
        django_get_or_create = ('slug',)

    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    title = 'first blog'
    slug = 'first-blog'
    overview = 'overview'
    content = 'content'
    thumbnail = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
