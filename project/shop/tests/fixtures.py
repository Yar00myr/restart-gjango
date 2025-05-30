import pytest

from shop.models import Category, Product


@pytest.fixture
def product():
    category = Category.objects.create(name="test_category")
    return Product.object.create(
        name="test_product",
        category=category,
        nomenclature="test_nomenclature",
        price=100,
    )


@pytest.fixture
def product_with_discount():
    category = Category.objects.create(name="test_category")
    return Product.object.create(
        name="test_product_2",
        category=category,
        nomenclature="test_nomenclature_2",
        price=100,
        discount=20,
    )
