from django.urls import path
from .views import home, about, product_details, cart_add, cart_details_view, cart_remove

app_name = "shop"


urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("product/<int:product_id>/", product_details, name="product_details"),
    path("cart_add/<int:product_id>/", cart_add, name="cart_add"),
    path("cart_details/", cart_details_view, name="cart_details"),
    path("cart_remove/<int:product_id>/", cart_remove, name="cart_remove"),
]
