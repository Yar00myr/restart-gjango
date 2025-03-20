from django.db import models


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
    discount = models.DecimalField(default=0.0,max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name}, {self.nomenclature}"

    class Meta:
        ordering = ["-created_at"]
        db_table = "products"
        unique_together = ["name", "description"]
