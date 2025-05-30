import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import Profile

@pytest.mark.django_db
def test_profile_creation():
    profile = Profile.objects.create()
    assert profile.avatar == 'avatars/washing_machine.jpg'