import pytest

from shop.serializers import ProductSerializer, OrderSerializer
from .fixtures import category, product_with_discount, product, order


@pytest.mark.django_db
def test_product_serializer_valid(category):
    data = {
        "name": "test_name",
        "description": "test_description",
        "entity": 2,
        "available": True,
        "category": category.id,
        "nomenclature": "test_nomenclature",
        "rating": 3,
        "attributes": {},
        "price": 100,
        "discount": 20,
    }
    serializer = ProductSerializer(data=data)

    assert serializer.is_valid()
    assert not serializer.errors


@pytest.mark.django_db
def test_product_serializer_invalid():
    data = {
        "name": "*" * 101,
        "description": {},
        "entity": -2,
        "available": 15,
        "nomenclature": "*" * 101,
        "rating": -3,
        "attributes": "*",
        "price": -100,
        "discount": -20,
    }
    serializer = ProductSerializer(data=data)

    assert not serializer.is_valid()
    print(serializer.data)
    print(dict(serializer.errors))
    assert serializer.errors
    for field in data.keys():
        assert field in serializer.errors
    assert (
        "Ensure this field has no more than 25 characters." in serializer.errors["name"]
    )
    assert "Must be a valid boolean." in serializer.errors["available"]
    assert (
        "Ensure this field has no more than 50 characters."
        in serializer.errors["nomenclature"]
    )
    assert "Rating must be >= 0" in serializer.errors["rating"]


@pytest.mark.django_db
def test_product_serializer_read_only(category):
    data = {
        "name": "test_name",
        "description": "test_description",
        "entity": 2,
        "available": True,
        "category": category.id,
        "nomenclature": "test_nomenclature",
        "rating": 3,
        "attributes": {},
        "price": 100,
        "discount": 20,
    }

    serializer = ProductSerializer(data=data)

    assert serializer.is_valid()
    assert "category" not in serializer.data


@pytest.mark.django_db
def test_product_serializer_method_field(product_with_discount):
    serializer = ProductSerializer(product_with_discount)

    assert serializer.data["discount_price"] == product_with_discount.discount_price
    assert serializer.data["discount_price"] == 80


@pytest.mark.django_db
def test_order_serializer_read_only(user, order):
    data = {
        "user": user.id,
        "contact_name": "test-name",
        "contact_phone": "0123456767",
        "contact_email": "test@gmail.com",
        "address": "test-address",
    }
    serializer = OrderSerializer(data=data)

    assert serializer.is_valid()
    assert "items" not in serializer.validated_data

    serializer = OrderSerializer(order)

    assert "items" in serializer.data


@pytest.mark.django_db
def test_order_serializer_items(order):

    serializer = OrderSerializer(order)

    items = serializer.data["items"]

    assert len(items) == 2
