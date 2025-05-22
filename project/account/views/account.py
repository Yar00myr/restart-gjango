from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from utils.email import send_confirmation_mail
from ..forms import RegisterForm, LoginForm, ProfileUpdateForm
from ..serializers import ProfileSerializer, UserSerializer, RegisterFormSerializer
from shop.models import Product, CartItem


class AccountViewSet(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @extend_schema(
        request=RegisterFormSerializer,
        responses={201: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    @action(detail=False, methods=["post"])
    def register(self, request):
        form = RegisterForm(request.data)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)
            send_confirmation_mail(request, user, user.email)
            return Response({"message": "User was registered"}, status=203)
        else:
            return Response({"errors": form.errors}, status=400)

    @action(detail=False, methods=["post"])
    def login_view(self, request):
        form = LoginForm(request.data)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.changed_data["password"],
            )
            if user:
                login(request, user)
                session_cart = request.session.get(settings.CART_SESSION_ID, default={})
                if session_cart:
                    cart = request.user.cart
                    for p_id, amount in session_cart.items():
                        product = Product.objects.get(id=p_id)
                        cart_item, created = CartItem.objects.get_or_create(
                            cart=cart, product=product
                        )
                        cart.amount = (
                            cart_item.amount + amount if not created else amount
                        )
                        cart_item.save()
                    session_cart.clear()
                return Response({"message": "Successful login"}, status=200)
            return Response({"error": "Incorrect login or password"}, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def logout_view(self, request):
        logout(request)
        return Response({"message": "Successfully logout"}, status=200)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def profile_view(self, request):
        profile = request.user.profile
        data = ProfileSerializer(profile).data
        return Response({"results": data}, status=200)

    @action(detail=True, methods=["put"], permission_classes=[IsAuthenticated])
    def edit_profile_view(self, request):
        profile = request.user.profile
        form = ProfileUpdateForm(request.data, request.FILES, user=request.user)
        if form.is_valid():
            new_email = form.changed_data.get("email")
            if new_email != request.user.email:
                send_confirmation_mail(request, request.user, new_email)

            avatar = form.cleaned_data.get("avatar")
            if avatar:
                profile.avatar = avatar
            profile.save()
            return Response({"results": ProfileSerializer(profile).data}, status=200)
        else:
            return Response(form.errors, status=400)

    @action(detail=True, methods=["get"])
    def confirm_email_view(self, request):
        user_id = request.GET.get("user")
        new_email = request.GET.get("email")
        if not user_id or not new_email:
            return Response({"error": "Invalid URL"}, status=400)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if user.is_active and User.objects.filter(email=new_email).exists():
            return Response({"error": "this email is already used"}, status=400)
        user.email = new_email
        user.is_active = True
        user.save()
        return Response({"results": UserSerializer(user).data}, status=200)
