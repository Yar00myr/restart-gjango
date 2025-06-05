import pytest

from shop.serializers import ProductSerializer
from .fixtures import category


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
        "attributes": [],
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
