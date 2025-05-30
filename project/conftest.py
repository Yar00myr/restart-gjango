import os
import pytest
import django

from django.contrib.auth.models import User
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


@pytest.fixture
def user():
    return User.objects.create_user(name="test_username", password="test_password")