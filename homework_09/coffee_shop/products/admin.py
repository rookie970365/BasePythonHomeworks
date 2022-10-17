from django.contrib import admin
from .models import Product, ProductProfile, ProductKind, ProductOrigin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    admin.site: admin.AdminSite


@admin.register(ProductKind)
class ProductKindAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(ProductOrigin)
class ProductOriginAdmin(admin.ModelAdmin):
    list_display = "pk", "origin"
    list_display_links = "pk", "origin"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "kind", "price", "description", "archived"
    list_display_links = "pk", "name", "price"
    ordering = "price", "pk",


@admin.register(ProductProfile)
class ProductProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "degree_of_roast", "preparation_method"
    list_display_links = "pk", "degree_of_roast", "preparation_method"
