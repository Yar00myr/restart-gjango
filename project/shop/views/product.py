from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)

from ..filters import ProductFilter
from ..models import Product, Category
from ..serializers import ProductSerializer


@extend_schema_view(
    list=extend_schema(
        description="**Get all products**",
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                description="Filter by **category**",
                examples=[
                    OpenApiExample(name=f"{category}", value=f"{category}")
                    for category in Category.objects.all()
                ],
                default="",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                description="Order products by **price and rating**",
                examples=[
                    OpenApiExample(name="Default", value="", description="No ordering"),
                    OpenApiExample(name="Increasing Price", value="price"),
                    OpenApiExample(name="Decreasing Price", value="-price"),
                    OpenApiExample(name="Increasing Rating", value="rating"),
                    OpenApiExample(name="Decreasing Rating", value="-rating"),
                ],
                default="",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                description="Search products by name or description.",
                examples=[
                    OpenApiExample(name="Search by keyword", value="laptop"),
                ],
            ),
        ],
    ),
    retrieve=extend_schema(description="Get details about certain product"),
    create=extend_schema(description="Create a product"),
    update=extend_schema(description="Update a product"),
    destroy=extend_schema(
        description="Delete a product",
    ),
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ["price", "rating"]
    search_fields = ["name", "description"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
