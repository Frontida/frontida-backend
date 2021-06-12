from rest_framework.serializers import ModelSerializer
from ..models import PurchaseInventory


class PurchaseInventorySerializers(ModelSerializer):
    class Meta:
        model = PurchaseInventory
        exclude = ["purchase", "isexpired"]
