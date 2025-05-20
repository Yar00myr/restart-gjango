from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.core.exceptions import ValidationError


from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
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

    def clean_price(self, value):
        if value <= 0:
            return ValidationError("The price should be higher than 0")
        else:
            return value
