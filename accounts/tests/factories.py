from django.contrib.auth.models import User

import factory


class UserFactory(factory.django.DjangoModelFactory):
    """
    Create new user instance.
    """
    class Meta:
        model = User
        django_get_or_create = ('email', 'username')

    username = 'testname'
    email = 'testemail@gmail.com'
    password = 'admin1600'
    is_active = True
