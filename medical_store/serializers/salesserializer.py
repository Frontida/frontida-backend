from rest_framework.serializers import ModelSerializer
from ..models import Sales, SalesInventory
from .salesinventoryserializers import SalesInventorySerializers
from rest_framework.response import Response


class SalesSerializers(ModelSerializer):
    salesinventory = SalesInventorySerializers(many=True)

    class Meta:
        model = Sales
        fields = [
            "customer_name",
            "customer_contact",
            "referred_by",
            "bill_date",
            "total_amount",
            "discount",
            "salesinventory",
        ]

    def validate(self, attrs):
        if attrs.get("customer_contact") not in range(6000000000, 9999999999):
            return Response({"error": "Invalid contact number"})
        return super().validate(attrs)

    def create(self, validated_data):
        sales_inventory_validated = validated_data.pop("salesinventory")
        sales = Sales.objects.create(**validated_data)
        for entry in sales_inventory_validated:
            SalesInventory.objects.create(sales_id=sales, **entry)
        return sales