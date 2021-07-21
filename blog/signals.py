from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from .models import Category, Post
from .utils import get_read_time


@receiver(pre_save, sender=Category)
def create_category_slug(sender, instance, **kwargs):
    """
    Create a slug for a category before saving.
    """
    instance.slug = slugify(instance.title, allow_unicode=True)


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, **kwargs):
    """
    Create a slug for a post before saving.
    """
    instance.slug = slugify(instance.title, allow_unicode=True)


@receiver(pre_save, sender=Post)
def set_post_read_time(sender, instance, **kwargs):
    """
    Set read time for a post before saving.
    """
    instance.read_time = get_read_time(instance.content)
