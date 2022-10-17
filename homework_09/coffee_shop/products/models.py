from django.db import models
from typing import TYPE_CHECKING


class ProductKind(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    kind = models.ForeignKey(ProductKind, on_delete=models.PROTECT, related_name="product")
    price = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True, null=False)
    origin = models.ManyToManyField("products.ProductOrigin", related_name="products")
    archived = models.BooleanField(default=False)

    if TYPE_CHECKING:
        objects: models.Manager

    def __str__(self):
        return self.name


class ProductProfile(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    degree_of_roast = models.CharField(max_length=64)
    preparation_method = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"Recommended coffee preparation methods: {self.preparation_method}"


class ProductOrigin(models.Model):
    origin = models.CharField(max_length=64)

    def __str__(self):
        return self.origin
