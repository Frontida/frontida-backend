from authentication.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
import uuid
from unittest import mock
from authentication.utils import Utils
from authentication.views import LoginAPI
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.test import Client, TestCase


class SigninTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create_user(
            email="test_1@gmail.com",
            password="test1234",
            user_type="MEDICAL STORE",
        )
        self.user_1.is_verified = True
        self.user_1.save()
        self.user_2 = User.objects.create_user(
            email="test_2@gmail.com", password="test1234", user_type="MEDICAL STORE"
        )

    def test_not_verified_user(self):
        request_url = "/auth/login/"
        response = self.client.post(
            request_url,
            {"email": self.user_2.email, "password": "test1234"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_not_exist(self):
        request_url = "/auth/login/"
        response = self.client.post(
            request_url,
            {"email": "shiva@gmail.com", "password": "test1234"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verified_user(self):
        request_url = "/auth/login/"
        response = self.client.post(
            request_url,
            {"email": self.user_1.email, "password": self.user_1.password},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
