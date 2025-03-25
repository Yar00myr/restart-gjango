from django.urls import path
from .views import home, about, product_details

app_name = "shop"


urlpatterns = [
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("product/<int:product_id>/", product_details, name="product_details"),
]
