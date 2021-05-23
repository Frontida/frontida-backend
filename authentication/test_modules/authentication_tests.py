from django.test import TestCase
from authentication.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
import uuid
from unittest import mock
from authentication.utils import Utils
from authentication.views import LoginAPI


class SigninTests(TestCase):
    def setUp(self):
        self.list_view = LoginAPI.as_view()
        self.user_1 = User.objects.create(
            email="test_1@gmail.com", password="test1234", is_verified=True
        )
        self.user_2 = User.objects.create(email="test_2@gmail.com", password="test1234")
        self.factory = APIRequestFactory()

    def test_not_verified_user(self):
        request_url = "/login/"
        create_request = self.factory.post(
            request_url,
            data={"email": self.user_2.email, "password": "test1234"},
            format="json",
        )
        response = self.list_view(
            create_request,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
