import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from shop.models import Product, Cart, CartItem, Category, Order, OrderItem
from .fixtures import product, product_with_discount, order, category


@pytest.mark.django_db
def test_product_model():
    category = Category.objects.create(name="test_category")
    product = Product.objects.create(
        name="test_product",
        category=category,
        nomenclature="test_nomenclature",
        price=100,
        discount=10,
    )

    assert product.discount_price == 90
    assert product.category.name == "test_category"


@pytest.mark.django_db
def test_cart_model_one_product(user, product):
    cart_item = CartItem.objects.create(cart=user.cart, product=product)
    assert cart_item.item_total == product.price
    assert user.cart.total == product.price


@pytest.mark.django_db
def test_cart_model_multiple_product(user, product):
    cart_item = CartItem.objects.create(cart=user.cart, product=product, amount=2)
    assert cart_item.item_total == product.price * 2
    assert user.cart.total == product.price * 2


@pytest.mark.django_db
def test_cart_model_discount_product(user, product_with_discount):
    cart_item = CartItem.objects.create(cart=user.cart, product=product_with_discount)
    assert cart_item.item_total == 80
    assert user.cart.total == 80


@pytest.mark.django_db
def test_cart_model_different_products(user, product, product_with_discount):
    cart_item = CartItem.objects.create(cart=user.cart, product=product)

    cart_item_2 = CartItem.objects.create(cart=user.cart, product=product_with_discount)
    assert user.cart.total == 180


@pytest.mark.django_db
def test_order_model_one_item(order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, price=product.price
    )
    assert order_item.amount == 1
    assert order_item.total_price == product.price


@pytest.mark.django_db
def test_order_model_multiple_items(order, product):
    order_item = OrderItem.objects.create(
        order=order, product=product, price=product.price, amount=2
    )
    assert order_item.amount == 2
    assert order_item.total_price == product.price * 2


@pytest.mark.django_db
def test_order_model_discount_item(order, product_with_discount):
    order_item = OrderItem.objects.create(
        order=order,
        product=product_with_discount,
        price=product_with_discount.discount_price,
    )

    assert order_item.total_price == 80


@pytest.mark.django_db
def test_order_model_different_items(order, product_with_discount, product):
    order_item_1 = OrderItem.objects.create(
        order=order, product=product, price=product.discount_price
    )

    order_item_2 = OrderItem.objects.create(
        order=order,
        product=product_with_discount,
        price=product_with_discount.discount_price,
    )

    assert order_item_1.total_price + order_item_2.total_price == 180
