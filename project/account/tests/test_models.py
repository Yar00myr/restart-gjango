import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from account.models import Profile
from shop.models import Cart


@pytest.mark.django_db
def test_profile_creation(user):
    # profile = Profile.objects.create(user=user)

    profile = Profile.objects.get(user=user)
    cart = Cart.objects.get(user=user)

    assert profile.avatar == "/avatars/washing_machine.jpg"
    assert profile.user == user
    assert cart.user == user
