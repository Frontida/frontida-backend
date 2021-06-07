from rest_framework.serializers import ModelSerializer
from ..models import Purchase, PurchaseInventory
from .purchaseinventoryserializer import PurchaseInventorySerializers

class PurchaseSerializers(ModelSerializer):

    purchaseinventory = PurchaseInventorySerializers(many=True)

    class Meta:
        model = Purchase
        fields = [
            "distributor_name",
            "bill_number",
            "bill_date",
            "total_amount",
            "discount",
            "company_name",
            "purchaseinventory",
        ]

    def create(self, validated_data):
        purchase_inventory_validated = validated_data.pop("purchaseinventory")
        purchase = Purchase.objects.create(**validated_data)
        for entry in purchase_inventory_validated:
            PurchaseInventory.objects.create(purchase=purchase, **entry)
        return purchase