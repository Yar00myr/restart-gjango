from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")

    if category_name:
        category = Category.objects.get(name=category_name)
        products = products.filter(category=category)

    match filter_name:
        case "price_increase":
            products = products.order_by("price")
        case "price_decrease":
            products = products.order_by("-price")
        case "rating_increase":
            products = products.order_by("rating")
        case "rating_decrease":
            products = products.order_by("-rating")
    return render(
        request, "shop/index.html", {"products": products, "categories": categories}
    )


def about(request):
    return render(request, "shop/about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_details.html", {"products": product})
