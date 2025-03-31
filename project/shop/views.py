from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    product_name = request.GET.get("search")
    category_name = request.GET.get("category")
    filter_name = request.GET.get("filter")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if start_date:
        products = products.filter(created_at__gte=start_date)

    if end_date:
        products = products.filter(created_at__lte=end_date)

    if product_name:
        products = products.filter(name__icontains=product_name)

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
            
    length = len(products)

    return render(
        request, "shop/index.html", {"products": products, "categories": categories, "length": length}
    )


def about(request):
    return render(request, "shop/about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_details.html", {"product": product})
