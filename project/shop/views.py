from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")

    if category_name:
        product = products.filter(category_name=category_name)

    if filter_name == "price_increase":
        product = product.order_by("price")
    elif filter_name == "price_decrease":
        product = product.order_by("-price")
    elif filter == "increase_rating":
        products = products.order_by("rating")
    else:
        products = products.order_by("-rating")
    return render(
        request, "shop/index.html", {"products": products, "categories": categories}
    )


def about(request):
    return render(request, "shop/about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_details.html", {"products": product})
