from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.authtoken.models import Token
from ..models import (
    CompanyDetails,
    MedicineInventory,
    Purchase,
    PurchaseInventory,
    Sales,
    SalesInventory,
)

from ..serializers import CompanyDetailsSerializers, MedicineInventorySerializers
from authentication.models import User


class CompanyDetailsViewSetTest(APITestCase):
    def setUp(self):
        self.data = {
            "company_name": "Cipla",
            "company_contact": 9809537756,
            "company_address": "Pune",
            "company_email": "cipla@gmail.com",
            "gst_number": "19ADE1",
        }
        self.test_company = CompanyDetails.objects.create(
            company_name="Pfizer",
            company_contact="8107662963",
            company_address="Pune",
            company_email="pfizer@gmail.com",
            gst_number="13DREF",
        )
        self.test_company_update_data = {
            "company_name": "Cipala",
            "company_contact": 9498392011,
            "company_address": "Mumbai",
            "company_email": "ciplaindia@gmail.com",
            "gst_number": "19BDE1",
        }
        self.user = User.objects.create(
            email="dummyuser@gmail.com", password="dummyuser", user_type="MEDICAL STORE"
        )
        self.admin = User.objects.create_superuser(
            email="dummyadmin@gmail.com",
            password="dummyadmin",
        )

    def test_create(self):
        url = reverse("medical_store:api-company-details-list")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With auth token of admin
        admin_token = Token.objects.get(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + admin_token.key)
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Comanay Details"), self.data)
        self.assertEqual(CompanyDetails.objects.count(), 2)

    def test_list(self):
        url = reverse("medical_store:api-company-details-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With proper auth token
        user_token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0], CompanyDetailsSerializers(self.test_company).data
        )

    def test_retreive(self):
        url = reverse(
            "medical_store:api-company-details-detail",
            kwargs={"pk": self.test_company.pk},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With proper auth
        user_token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, CompanyDetailsSerializers(self.test_company).data
        )

        # With proper auth bit company with given pk dosent exist
        url = reverse("medical_store:api-company-details-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("error"), "Company with given pk not found")

    # def test_update(self):
    #     url = reverse("medical_store:api-company-details-detail", kwargs={"pk": self.test_company.pk})
    #     response = self.client.put(url, self.test_company_update_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(str(response.data.get("detail")), "Authentication credentials were not provided.")

    #     # With proper auth
    #     user_token = Token.objects.get(user=self.user)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_token.key)
    #     response = self.client.put(url, self.test_company_update_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, CompanyDetailsSerializers(self.test_company).data)

    #     # With proper auth bit company with given pk dosent exist

    # def test_partialupdate(self):
    #     pass

    # def test_destroy(self):
    #     pass


class MedicineInventoryViewSetTest(APITestCase):
    def setUp(self):
        self.test_company = CompanyDetails.objects.create(
            company_name="Pfizer",
            company_contact="8107662963",
            company_address="Pune",
            company_email="pfizer@gmail.com",
            gst_number="13DREF",
        )

        self.test_user = User.objects.create(
            email="dummyuser@gmail.com", password="dummyuser", user_type="MEDICAL STORE"
        )

        self.test_medicine_inventory = MedicineInventory.objects.create(
            HSNcode="BEXC12",
            batch_number="A32",
            medicine_name="Diclovin-plus",
            company_name=self.test_company,
            mfd="2021-04-03",
            expiry="2024-04-02",
            purchase_price=8,
            sale_price=10,
            medicine_quantity=100,
            account=self.test_user,
            isexpired=False,
        )

    def test_list(self):
        # Without auth
        url = reverse("medical_store:api-medical-inventory-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With auth
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        url = reverse("medical_store:api-medical-inventory-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data.get("medicine_inventory")[0],
            MedicineInventorySerializers(self.test_medicine_inventory).data,
        )


class PurchaseViewSetsTest(APITestCase):
    def setUp(self):
        self.test_company = CompanyDetails.objects.create(
            company_name="Pfizer",
            company_contact="8107662963",
            company_address="Pune",
            company_email="pfizer@gmail.com",
            gst_number="13DREF",
        )

        self.test_user = User.objects.create(
            email="dummyuser@gmail.com", password="dummyuser", user_type="MEDICAL STORE"
        )

        self.purchase = Purchase.objects.create(
            distributor_name="test distributor",
            company_name="Pfizer",
            bill_number="TB10023",
            bill_date="2021-04-30",
            total_amount=300,
            discount=10,
            account=self.test_user,
        )

        self.purchase_inventory1 = PurchaseInventory.objects.create(
            medicine_name="testMedicine 1",
            quantity=100,
            batch_number="B234",
            price_of_each=1,
            mrp=2,
            mfd="2021-04-03",
            expiry="2023-04-02",
            purchase=self.test_purchase,
        )

        self.purchase_inventory1 = PurchaseInventory.objects.create(
            medicine_name="testMedicine 2",
            quantity=100,
            batch_number="CX34",
            price_of_each=2,
            mrp=3,
            mfd="2021-03-27",
            expiry="2023-11-02",
            purchase=self.test_purchase,
        )

    def test_list(self):
        # Without auth
        url = reverse("medical_store:api-purchase-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With auth
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
