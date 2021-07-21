from django.contrib import admin

from .models import Category, Post


# models admin site registeration
admin.site.register(Category)
admin.site.register(Post)
