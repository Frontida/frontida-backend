from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from ..models import (
    CompanyDetails,
    MedicineInventory,
    Purchase,
    PurchaseInventory,
    Sales,
    SalesInventory,
)
from ..serializers import (
    CompanyDetailsSerializers,
    MedicineInventorySerializers,
    PurchaseSerializers,
    SalesSerializers,
)
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
            purchase=self.purchase,
        )

        self.purchase_inventory1 = PurchaseInventory.objects.create(
            medicine_name="testMedicine 2",
            quantity=100,
            batch_number="CX34",
            price_of_each=2,
            mrp=3,
            mfd="2021-03-27",
            expiry="2023-11-02",
            purchase=self.purchase,
        )

        MedicineInventory.objects.bulk_create(
            [
                MedicineInventory(
                    HSNcode="BEXC12",
                    batch_number="B234",
                    medicine_name="testMedicine 1",
                    company_name=self.test_company,
                    mfd="2021-04-03",
                    expiry="2023-04-02",
                    purchase_price=1,
                    sale_price=2,
                    medicine_quantity=100,
                    account=self.test_user,
                    isexpired=False,
                ),
                MedicineInventory(
                    HSNcode="BEXC12",
                    batch_number="CX34",
                    medicine_name="testMedicine 2",
                    company_name=self.test_company,
                    mfd="2021-03-27",
                    expiry="2023-11-02",
                    purchase_price=2,
                    sale_price=3,
                    medicine_quantity=100,
                    account=self.test_user,
                    isexpired=False,
                ),
            ]
        )

        self.data = {
            "distributor_name": "Kshitizg Distributor",
            "bill_number": "175ET",
            "bill_date": "2020-10-23",
            "company_name": "Sunpharma",
            "total_amount": 1700,
            "discount": 5,
            "purchaseinventory": [
                {
                    "medicine_name": "paracetamol",
                    "quantity": 100,
                    "batch_number": "12R4T",
                    "price_of_each": 2,
                    "mrp": 3,
                    "mfd": "2021-01-01",
                    "expiry": "2024-01-01",
                },
                {
                    "medicine_name": "diclovinplus",
                    "quantity": 100,
                    "batch_number": "98CTU",
                    "price_of_each": 15,
                    "mrp": 17,
                    "mfd": "2021-01-01",
                    "expiry": "2024-01-01",
                },
            ],
        }

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
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data.get("previousbills")[0].get("purchaseinventory")), 2
        )
        self.assertEqual(len(response.data.get("companynames")), 1)
        self.assertEqual(
            response.data.get("previousbills")[0],
            PurchaseSerializers(self.purchase).data,
        )
        self.assertEqual(
            response.data.get("companynames")[0],
            CompanyDetailsSerializers(self.test_company).data.get("company_name"),
        )

    def test_create(self):
        url = reverse("medical_store:api-purchase-list")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With valid auth token
        # Invalid company name
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("error"), "Invalid company name")

        # With Valid company name and auth token
        # Purchased medicine dosent have the same batch number and name as some other medicine in the inventory
        self.data["company_name"] = "Pfizer"
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Purchase.objects.count(), 2)
        self.assertEqual(MedicineInventory.objects.count(), 4)

        # With vlaid company name
        # This time the there exist medicines in the medicine inventory with the same bathch and name as those purchased
        # Update data for test case
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Purchase.objects.count(), 3)
        self.assertEqual(MedicineInventory.objects.count(), 4)
        self.assertEqual(
            MedicineInventory.objects.get(batch_number="12R4T").medicine_quantity, 200
        )
        self.assertEqual(
            MedicineInventory.objects.get(batch_number="98CTU").medicine_quantity, 200
        )
        print(response.data.get("purchaseinventory")[0].get("medicine_name"))
        print(response.data.get("purchaseinventory")[1].get("medicine_name"))
        self.assertEqual(
            response.data.get("purchaseinventory")[0].get("medicine_name"),
            "paracetamol",
        )
        self.assertEqual(
            response.data.get("purchaseinventory")[1].get("medicine_name"),
            "diclovinplus",
        )

    def test_retrieve(self):
        url = reverse(
            "medical_store:api-purchase-detail", kwargs={"pk": self.purchase.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With auth token
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PurchaseSerializers(self.purchase).data)


class SalesViewSetsTest(APITestCase):
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

        self.sales = Sales.objects.create(
            bill_number="BN123",
            customer_name="test customer1",
            customer_contact=9987654321,
            referred_by="test doctor1",
            bill_date="2021-05-22",
            total_amount=13,
            discount=10,
            account=self.test_user,
        )

        (
            self.sales_inventory1,
            self.sales_inventory2,
        ) = SalesInventory.objects.bulk_create(
            [
                SalesInventory(
                    medicine_name="testMedicine 1",
                    quantity=10,
                    batch_number="124E",
                    price_of_each=2,
                    sales_id=self.sales,
                ),
                SalesInventory(
                    medicine_name="testMedicine 2",
                    quantity=10,
                    batch_number="AE34",
                    price_of_each=3,
                    sales_id=self.sales,
                ),
            ]
        )

        MedicineInventory.objects.bulk_create(
            [
                MedicineInventory(
                    HSNcode="BEXC12",
                    batch_number="B234",
                    medicine_name="testMedicine 1",
                    company_name=self.test_company,
                    mfd="2021-04-03",
                    expiry="2023-04-02",
                    purchase_price=1,
                    sale_price=2,
                    medicine_quantity=20,
                    account=self.test_user,
                    isexpired=False,
                ),
                MedicineInventory(
                    HSNcode="BEXC12",
                    batch_number="CX34",
                    medicine_name="testMedicine 2",
                    company_name=self.test_company,
                    mfd="2021-03-27",
                    expiry="2023-11-02",
                    purchase_price=2,
                    sale_price=3,
                    medicine_quantity=10,
                    account=self.test_user,
                    isexpired=False,
                ),
            ]
        )

        self.data = {
            "customer_name": "Test customer 1",
            "customer_contact": 9829085405,
            "referred_by": "Test doctor 1",
            "total_amount": 20,
            "bill_date": "2021-05-22",
            "discount": 0,
            "salesinventory": [
                {
                    "medicine_name": "testMedicine 3",
                    "quantity": 30,
                    "batch_number": "B234",
                    "price_of_each": 2,
                },
                {
                    "medicine_name": "testMedicine 2",
                    "quantity": 10,
                    "batch_number": "CX34",
                    "price_of_each": 2,
                },
            ],
        }

    def test_list(self):
        # Without auth
        url = reverse("medical_store:api-sales-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With auth token
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("previoussales")[0], SalesSerializers(self.sales).data
        )

    def test_create(self):
        # Without auth
        url = reverse("medical_store:api-sales-list")
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With proper auth but required medicine is not available in medicine inventory
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("medicine"), "not found")

        # With proper auth and medicine available in inventory but not in required amount
        # Updating the medicine name in data
        self.data["salesinventory"][0]["medicine_name"] = "testMedicine 1"
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("medicine"), "not enough stock")

        # With proper auth and the medicine is available in iventory in the required quantity
        # Updating the required quantity in the data
        self.data["salesinventory"][0]["quantity"] = 10
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MedicineInventory.objects.count(), 1)
        self.assertEqual(
            MedicineInventory.objects.all()[0].medicine_name, "testMedicine 1"
        )
        self.assertEqual(MedicineInventory.objects.all()[0].medicine_quantity, 10)
        self.assertEqual(response.data.get("customer_name"), "Test customer 1")
        self.assertEqual(
            response.data.get("salesinventory")[0]["medicine_name"], "testMedicine 1"
        )
        self.assertEqual(
            response.data.get("salesinventory")[1]["medicine_name"], "testMedicine 2"
        )

    def test_retrieve(self):
        # Without auth
        url = reverse("medical_store:api-sales-detail", kwargs={"pk": self.sales.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            str(response.data.get("detail")),
            "Authentication credentials were not provided.",
        )

        # With auth credentials but wrong primary key
        url = reverse(
            "medical_store:api-sales-detail", kwargs={"pk": self.sales.pk + 1}
        )
        user_token = Token.objects.get(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("doesNotExist"), "does not exist in database"
        )

        # With auth credentials and proper primary key
        url = reverse("medical_store:api-sales-detail", kwargs={"pk": self.sales.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("salesinventory")), 2)
        self.assertEqual(response.data.get("customer_name"), "test customer1")
        self.assertEqual(
            response.data.get("salesinventory")[1]["medicine_name"], "testMedicine 2"
        )
