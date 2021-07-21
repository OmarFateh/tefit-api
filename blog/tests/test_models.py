import os

from django.conf import settings

from blog.models import Post


class TestModel:

    def test_category_str(self, new_category):
        """
        Test category obj str method.
        """
        assert new_category.__str__() == 'fitness'

    def test_post_str(self, new_post):
        """
        Test post obj str method.
        """
        assert new_post.__str__() == 'first blog'

    def test_post_published_list(self, new_post):
        """
        Test get published post list of post manager.
        """
        assert Post.objects.filter(status='published').count(
        ) == Post.objects.get_published_posts_list().count()

    def test_post_thumbnail_upload_path(self, new_post):
        """
        Test upload path of post thumbnail.
        """
        photo_name = new_post.thumbnail.name.split('/')[-1]
        photo_path = os.path.join(
            settings.BASE_DIR, f'media\\posts\\first blog\\{photo_name}')
        assert new_post.thumbnail.path == photo_path
