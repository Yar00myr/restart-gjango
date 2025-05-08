from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Cart, CartItem, Product
from ..serializers import CartItemSerializer, CartSerializer, ProductSerializer


class CartViewSet(ModelViewSet):
    @action(detail=False, methods=["post"], url_path="add-product/<product_id>/")
    def add(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = request.user.cart
            cart = Cart.objects.get(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                product=product, cart=cart
            )
            if created:
                cart_item.amount = 1
            else:
                cart_item.amount += 1
            cart_item.save()
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            cart[str(product_id)] = cart.get(str(product_id), default=0) + 1
        return Response(
            {"message": f"product with id:{product_id} successfully added"}, status=200
        )

    @action(detail=False, methods=["get"], url_path="get-cart-items/")
    def detail(self, request):
        if request.user.is_authenticated:
            cart = request.user.cart
            return Response(CartSerializer(cart).data)
        else:
            cart = request.session.get(settings.CART_SESSION_ID, default={})
            products = Product.objects.filter(id__in=cart.keys())
            # fields = ["cart", "product", "item_total", "amount"] items
            # fields = ["user", "created_at", "items", "total"] cart
            items = []
            total = 0
            for product in products:
                data = ProductSerializer(product).data
                amount = cart.get(str(product.id))
                item_total = (product.discount_price or product.price) * amount
                items.append(
                    {
                        "product": data,
                        "amount": amount,
                        "item_total": item_total,
                        "cart": None,
                    }
                )
                total += item_total
            return Response(
                {
                    "user": request.user,
                    "created_at": None,
                    "items": items,
                    "total": total,
                }
            )
