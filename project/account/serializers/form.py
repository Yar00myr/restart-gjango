from django.contrib.auth.models import User
from rest_framework import serializers
from .captcha import CaptchaFieldSerializer


class RegisterFormSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    captcha = CaptchaFieldSerializer(required=True)
