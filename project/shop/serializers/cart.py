from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


from ..models import Cart, CartItem
from .product import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["cart", "product", "item_total", "amount"]

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_item_total(self, obj):
        return obj.item_total


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cart_items", many=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ["user", "created_at", "items", "total"]

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total(self, obj) -> float:
        return obj.total
