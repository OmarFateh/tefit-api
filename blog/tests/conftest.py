import pytest
from rest_framework.test import APIClient, APIRequestFactory
from pytest_factoryboy import register

from accounts.tests.factories import UserFactory
from .factories import CategoryFactory, PostFactory

register(UserFactory)
register(CategoryFactory)
register(PostFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.fixture
def new_user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def new_category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def new_post(db, post_factory):
    post = post_factory.create()
    return post
