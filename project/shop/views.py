from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Payment
from .forms import OrderCreateForm

from utils.email import send_order_confirmation_email


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
    context = {"products": products, "categories": categories, "length": length}
    return render(request, "shop/index.html", context=context)


def about(request):
    return render(request, "shop/about.html")


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_details.html", {"product": product})


def cart_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        if cart.get(product_id):
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.amount += 1
            cart_item.save()
    return redirect("shop:cart_details")


def cart_details_view(request):
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        products_id = cart.keys()
        products = Product.objects.filter(id__in=products_id)
        cart_items = []
        total_price = 0
        for product in products:
            count = cart[str(product.id)]
            price = count * product.price
            total_price += price
            cart_items.append({"product": product, "count": count, "price": price})
    else:
        try:
            cart = request.user.cart

        except Cart.DoesNotExist:
            cart = None

        if not cart or not cart.items.count():
            cart_items = []
            total_price = 0
        else:
            cart_items = cart.items.select_related("product").all()
            total_price = sum(item.product.price * item.amount for item in cart_items)

    return render(
        request,
        "shop/cart_detail.html",
        {"cart_items": cart_items, "total_price": total_price},
    )


def cart_remove(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    if not request.user.is_authenticated:
        cart = request.session.get(settings.CART_SESSION_ID, {})
        cart.pop(str(product_id), None)
        request.session[settings.CART_SESSION_ID] = cart
    else:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_item = cart.items.filter(product=product).first()
            if cart_item:
                cart_item.delete()
    return redirect("shop:cart_details")


def calculate_discount(value, arg):
    discount_value = value * arg / 100
    return value - discount_value


def checkout(request):
    if (request.user.is_authenticated and not getattr(request.user, "cart", None)) or (
        not request.user.is_authenticated
        and not request.session.get(settings.CART_SESSION_ID)
    ):
        messages.error(request, "cart is empty")
        return redirect("shop:cart_detail")
    if request.method == "GET":
        form = OrderCreateForm()
        if not request.user.is_authenticated:
            form.initial["contact_email"] = request.user.email
    elif request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order, user = request.user
            order.save()

            if request.user.is_authenticated:
                cart = getattr(request.user, "cart")
                cart_items = cart.items.select_related("product").all()
            else:
                cart = request.session.get(settings.CART_SESSION_ID)
                cart_items = []
                for product_id, amount in cart.items():
                    product = Product.objects.get(id=product_id)
                    cart_items.append({"product": product}, {"amount": amount})

            items = OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        product=item.product,
                        amount=item.amount,
                        price=calculate_discount(
                            item.product.price, item.product.discount
                        ),
                    )
                    for item in cart_items
                ]
            )
            
            total_price = sum(item.product*item.amount for item in items)
            method = form.cleaned_data.get("payment_method")
            if method != "cash":
                Payment.objects.create(order=order, provider=method, amount=total_price)
            else:
                order.status = 2
            order.save()
            
            
            if request.user.is_authenticated:
                cart.items.all().delete()
            else:
                request.session[settings.CART_SESSION_ID] = {}
                send_order_confirmation_email(order=order)
                messages.success(request, "Text")
                return redirect("shop:index")

    return render(request, "shop/checkout.html", {"form": form})
