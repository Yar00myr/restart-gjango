
from rest_framework import serializers


class CaptchaFieldSerializer(serializers.Serializer):
    captcha_0 = serializers.CharField(required=True)
    captcha_1 = serializers.CharField(required=True)

    def validate(self, attrs):
        from captcha.models import CaptchaStore
        # from captcha.helpers import captcha_image_url

        try:
            captcha = CaptchaStore.objects.get(hashkey=attrs["captcha_0"])

        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Incorrect captcha")

        if captcha.response != attrs.get("captcha_1", "").lower():
            raise serializers.ValidationError("Invalid captcha")

        captcha.delete()
        return attrs
