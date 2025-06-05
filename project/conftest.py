import os
import pytest
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


@pytest.fixture
def user():
    return django.contrib.auth.models.User.objects.create_user(
        username="test_username", password="test_password"
    )
