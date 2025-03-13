from django.urls import path
from .views import home, about

app_name = "shop"


urlpatterns = [
    path("home/", home, name="home"),
    path("about/", about, name="about"),
]
