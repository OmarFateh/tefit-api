import json
import os

from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.models import Category, Post


class TestCategory:

    category_list_endpoint = reverse('blog-api:category-list')
    category_create_endpoint = reverse('blog-api:category-create')
    category_posts_list_endpoint = reverse(
        'blog-api:category-posts-list', kwargs={"slug": 'fitness'})
    category_detail_endpoint = reverse(
        'blog-api:category-detail', kwargs={"slug": 'fitness'})
    data = {'title': 'food'}

    def test_category_list(self, db, new_category, api_client):
        """
        Test category retrieve list response status.
        """
        response = api_client.get(self.category_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_category_posts_list(self, db, new_category, new_post, api_client):
        """
        Test category retrieve posts list response status.
        """
        response = api_client.get(
            self.category_posts_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_category_create(self, db, new_user, api_client):
        """
        Test category create response status.
        """
        api_client.force_authenticate(new_user)
        assert Category.objects.count() == 0
        response = api_client.post(
            self.category_create_endpoint, self.data, format='json')
        assert response.status_code == 201
        assert Category.objects.count() == 1

    def test_category_update(self, db, new_user, new_category, api_client):
        """
        Test category update response status.
        """
        api_client.force_authenticate(new_user)
        assert new_category.title == 'fitness'
        response = api_client.put(
            self.category_detail_endpoint, self.data, format='json')
        new_category.refresh_from_db()
        assert response.status_code == 200
        assert new_category.title == 'food'

    def test_category_delete(self, db, new_user, new_category, api_client):
        """
        Test category delete response status.
        """
        api_client.force_authenticate(new_user)
        assert Category.objects.count() == 1
        response = api_client.delete(self.category_detail_endpoint)
        assert response.status_code == 204
        assert Category.objects.count() == 0


class TestPosts:

    post_list_endpoint = reverse('blog-api:post-list')
    post_create_endpoint = reverse('blog-api:post-create')
    post_detail_endpoint = reverse(
        'blog-api:post-detail', kwargs={"slug": 'first-blog'})
    upload_file = open(os.path.join(settings.BASE_DIR,
                                    'static/img/no_avatar.jpg'), "rb")
    thumbnail = SimpleUploadedFile(
        name='no_avatar.jpg', content=upload_file.read(), content_type='image/jpeg')
    data = {'title': 'new', 'author': 1, 'category': 1, 'status': 'published',
            'overview': 'new', 'content': 'new', 'thumbnail': thumbnail}

    def test_post_list(self, db, new_post, api_client):
        """
        Test post retrieve list response status.
        """
        response = api_client.get(self.post_list_endpoint, format='json')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_post_create(self, db, new_user, new_category, api_client):
        """
        Test post create response status.
        """
        api_client.force_authenticate(new_user)
        assert Post.objects.count() == 0
        response = api_client.post(
            self.post_create_endpoint, self.data, format='multipart')
        assert response.status_code == 201
        assert Post.objects.count() == 1

    def test_post_detail(self, db, new_post, api_client):
        """
        Test detail post retrieve response status.
        """
        response = api_client.get(self.post_detail_endpoint, format='json')
        assert response.status_code == 200

    def test_post_delete(self, db, new_user, new_post, api_client):
        """
        Test post delete response status.
        """
        api_client.force_authenticate(new_user)
        assert Post.objects.count() == 1
        response = api_client.delete(self.post_detail_endpoint)
        assert response.status_code == 204
        assert Post.objects.count() == 0
