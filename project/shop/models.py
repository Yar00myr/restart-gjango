from django.db import models
from django.contrib.auth.models import User


class Seller(models.Model):
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

    def __repr__(self):
        return f"{self.name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
        db_table = "categories"


class Product(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(null=True, blank=True)
    entity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    nomenclature = models.CharField(unique=True, max_length=50)
    image_path = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    attributes = models.JSONField(default=dict)
    price = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    discount = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)

    @property
    def discount_price(self):
        if self.discount:
            return round(self.price - (self.price * self.discount / 100), 2)

    def __str__(self):
        return f"{self.name}, {self.nomenclature}"

    class Meta:
        ordering = ["-created_at"]
        db_table = "products"
        unique_together = ["name", "description"]


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return sum([item.item_total for item in self.items.all()])
    
    def __str__(self):
        return f"{self.user.username}'s cart "


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def item_total(self):
        return (
            self.product.price * self.amount
            if not self.product.discount
            else self.product.discount_price * self.amount
        )

    def __str__(self):
        return f"{self.product.name} : {self.amount}"


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20, default="000-000-0000")
    contact_email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.IntegerChoices):
        NEW = 1
        PROCESSING = 2
        SHIPPED = 3
        COMPLETED = 4
        CANCELED = 5

    status = models.IntegerField(choices=Status, default=Status.NEW)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.amount

    def __str__(self):
        return f"{self.order.id} : {self.product.name} : {self.amount} : {self.price}"


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    provider = models.CharField(
        max_length=20,
        choices={"liqpay": "LiqPay", "monopay": "MonoPay", "google": "Google Pay"},
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Status(models.IntegerChoices):
        PENDING = 1
        PAID = 2
        FAILED = 3

    status = models.IntegerField(choices=Status, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, blank=100)
    created_at = models.DateTimeField(auto_now_add=True)
