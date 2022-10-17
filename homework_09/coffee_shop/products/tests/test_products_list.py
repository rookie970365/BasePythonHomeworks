from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse_lazy


class ProductsListTestCase(TestCase):
    fixtures = [
        "product_origins.fixture.json",
        "product_kinds.fixture.json",
        "products.fixture.json",
    ]

    url = reverse_lazy("products:index")

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anon_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context["user"].is_anonymous)
