from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.core.exceptions import ValidationError


from ..models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "entity",
            "available",
            "category",
            "nomenclature",
            "created_at",
            "rating",
            "attributes",
            "price",
            "discount",
            "discount_price",
        ]

    @extend_schema_field(OpenApiTypes.FLOAT)
    def get_discount_price(self, obj):
        return obj.discount_price

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("The price should be higher than 0")
        return value

    def clean_description(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Description must be a str")
        return value

    def validate_rating(self, value):
        if value < 0:
            raise serializers.ValidationError("Rating must be >= 0")
        return value

    def validate_attributes(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Attributes must be a dictionary.")
        else:
            return value

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError("Discount must be >= 0")
        return value
