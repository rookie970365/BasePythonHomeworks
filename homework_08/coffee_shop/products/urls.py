from django.urls import path
from .views import (
    # index,
    # details,
    ProductsListView,
    ProductDetailView,
)
app_name = "products"

urlpatterns = [
    # path("", index, name="index"),
    # path("<int:pk>/", details, name="details"),
    path("", ProductsListView.as_view(), name="index"),
    path("<int:pk>/", ProductDetailView.as_view(), name="details")
]
