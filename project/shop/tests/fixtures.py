import pytest

from shop.models import Category, Product, Order, OrderItem


@pytest.fixture
def product(category):

    return Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test_nomenclature",
        price=100,
    )


@pytest.fixture
def category():
    return Category.objects.create(name="test_category")


@pytest.fixture
def product_with_discount(category):

    return Product.objects.create(
        name="test_product_2",
        category=category,
        nomenclature="test_nomenclature_2",
        price=100,
        discount=20,
    )


@pytest.fixture
def order(user, product, product_with_discount):
    order_ = Order.objects.create(
        user=user,
        contact_name="test_contact_name_1",
        contact_phone="+00000001",
        contact_email="test_contact_email1@gmail.com",
        address="test_address_field_1",
    )

    OrderItem.objects.create(order=order_, product=product, price=100)

    OrderItem.objects.create(
        order=order_, product=product_with_discount, amount=2, price=80
    )

    return order_
