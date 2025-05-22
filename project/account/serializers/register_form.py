from django.contrib.auth.models import User
from rest_framework import serializers
from .captcha import CaptchaFieldSerializer


class RegisterFormSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    captcha = CaptchaFieldSerializer()

    class Meta:
        model = User
        extra_fields = ["email"]
        fields = ["username", "password1", "password2"]
