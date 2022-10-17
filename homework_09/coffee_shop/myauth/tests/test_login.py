from http import HTTPStatus
from random import choices
from string import ascii_letters, digits

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AbstractUser
from myauth.models import UserModel


class LoginTestCase(TestCase):
    url = reverse_lazy("myauth:login")
    secret_url = reverse_lazy("myauth:secret")

    def setUp(self) -> None:
        password = "".join(choices(ascii_letters + digits, k=10))
        username = "".join(choices(ascii_letters, k=15))
        # user: AbstractUser = UserModel.objects.create_user(
        #      username=username, password=password)
        user = get_user_model().objects.create_user(username=username, password=password)
        # self.user.save()
        self.user = user
        self.password = password
        print("+++++++++ user create")

    def tearDown(self):
        print("------- user delete")
        self.user.delete()

    def test_correct(self):
        user = authenticate(username=self.user.username, password=self.password)
        self.assertTrue(user is not None and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password=self.password)
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username=self.user.username, password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_login(self):
        response_auth = self.client.post(self.url, {"username": self.user.username, "password": self.password})
        self.assertEqual(response_auth.url, reverse("myauth:me"))
        response_page = self.client.get(response_auth.url)
        user = response_page.context["user"]
        self.assertFalse(user.is_anonymous)
        self.assertEqual(user.username, self.user.username)

    def test_anon_access_to_secret_page_is_restricted(self):
        response = self.client.get(self.secret_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_authorised_access_to_secret_page(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.secret_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register(self):
        url = reverse_lazy("myauth:register")
        self.client.post(url, {"username": self.user.username,
                               "password": self.password,
                               "email": str(self.user.username)+"@gmail.com",
                               "password2": self.password})
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(self.url)
        self.assertFalse(response.context["user"].is_anonymous)
        # user = authenticate(username=self.user.username, password=self.password)
        # print(user, response.context["user"])
        # self.assertTrue(user is not None and user.is_authenticated)


