from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CartViewSet
from .views.views import (
    home,
    about,
    product_details,
    cart_add,
    cart_details_view,
    cart_remove,
    checkout,
)

app_name = "shop"

router = DefaultRouter()
router.register(prefix=r"categories", viewset=CategoryViewSet, basename="category")
router.register(prefix=r"products", viewset=ProductViewSet, basename="product")
router.register(prefix=r"carts", viewset=CartViewSet, basename="cart")

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("product/<int:product_id>/", product_details, name="product_details"),
    path("cart/cart-add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart_details/", cart_details_view, name="cart_details"),
    path("cart_remove/<int:product_id>/", cart_remove, name="cart_remove"),
    path("checkout/", checkout, name="checkout"),
]

urlpatterns += router.urls
