import pytest

from django.urls import reverse

from .fixtures import category, product, product_with_discount


@pytest.mark.django_db
def test_products_list_empty(api_client):
    url = reverse("shop:product-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_products_list(api_client, product, product_with_discount):
    url = reverse("shop:product-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_products_detail(api_client, product):
    url = reverse("shop:product-detail", kwargs={"pk": product.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == product.name
