import pytest
import uuid

from django.contrib.auth.models import User
from django.urls import reverse

from .fixtures import category, product, product_with_discount
from shop.models import Product


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


@pytest.mark.django_db
def test_product_detail_not_found(api_client):
    url = reverse("shop:product-detail", kwargs={"pk": 1435768})

    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_product_update_not_authorized(api_client, product):
    url = reverse("shop:product-detail", kwargs={"pk": product.id})

    response = api_client.patch(url, data={"price": 200})

    assert response.status_code == 403


@pytest.mark.django_db
def test_update_product(api_client, super_user, product):
    api_client.force_authenticate(super_user)
    url = reverse("shop:product-detail", kwargs={"pk": product.pk})

    response = api_client.patch(url, data={"price": 100}, format="json")

    assert response.status_code == 200
    assert float(response.data.get("price")) == 100
    assert product.price == 100


@pytest.mark.django_db
def test_create_product(api_client, super_user, category):
    url = reverse("shop:product-list")
    data = {
        "name": "test_name_1",
        "description": "test_description_1",
        "entity": 1,
        "category": category.id,
        "nomenclature": str(uuid.uuid4()),
    }

    api_client.force_authenticate(super_user)
    response = api_client.post(url, data=data)

    assert response.status_code == 201
    assert response.data.get("name") == "test_name"
    assert Product.objects.filter(id=response.data.get("id")).exists()


@pytest.mark.django_db
def test_product_create_not_authorized(api_client, category):
    url = reverse("shop:product-list")

    data = {
        "name": "test-product",
        "category": category.id,
        "nomenclature": uuid.uuid4(),
    }

    response = api_client.post(url, data=data)

    assert response.status_code == 403
